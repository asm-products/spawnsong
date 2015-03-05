import os
import shlex
import shutil
import subprocess
import tempfile
import time

import requests
from celery.utils.log import get_task_logger
from django.conf import settings
from django.core.files import File
from django.db import transaction

import models
from sites.spawnsongsite.celery import app


logger = get_task_logger("media.tasks")

@app.task(bind=True,retries=3)
def transcode_audio(self, audioformat_id, profile):
    # print "Transcode?"
    print ("Transcoding!")
    logger.info("Transcoding audio for audio format id %s" % (audioformat_id,))
    
    tmpdir = tempfile.mkdtemp()
    audioformat = models.AudioFormat.objects.get(pk=audioformat_id)
    try:
        infile = os.path.join(tmpdir, "input")
        outfile = os.path.join(tmpdir, "output.mp3")
        print ("Downloading data")
        open(infile, "wb").write(audioformat.audio.original.read())
        print ("Running ffmpeg")
        command = shlex.split(profile["command"].format(input=infile, output=outfile))
        print command
        returncode = subprocess.call(command)
        # print returncode
        if returncode != 0:
            logger.error("ffmpeg returned code: %s" % (returncode,))
            audioformat.last_error="Failed to encode audio, ffpmeg returned code: %s" % (returncode,)
            audioformat.save()
            return self.retry()
        print ("Saving transcoded audio")
        
        audioformat.audio_data.save("audio.%s" % (profile["extension"],), File(open(outfile, "rb")))
        audioformat.state = "ready"
        audioformat.save()
    finally:
        print ("Cleaing up temporary directory")
        shutil.rmtree(tmpdir)
    print ("Done transcoding")
    return True

@app.task(bind=True)
def transcode_audio_failed(self, audioformat_id):
    models.AudioFormat.objects.filter(pk=audioformat_id).update(state="failed")

@app.task(bind=True,retries=3)
def request_echonest_data(self, audio_id):
    audio = models.Audio.objects.get(pk=audio_id)
    
    print "Echonest!"
    logger.debug("Transcoding!")
    try:
        response = requests.post(
            "http://developer.echonest.com/api/v4/track/upload",
            data={"url": audio.original.url, "api_key": settings.ECHONEST_API_KEY})
    
        echonest_id = response.json()["response"]["track"]["id"]
    except:
        logger.error("Bad response from echonest upoad: %s" % (response.text,))
        self.retry()
   
    print "Check response"
    try:
        audio = models.Audio.objects.get(pk=audio.pk)
    except models.Audio.DoesNotExist:
        logger.warn("Can't find Audio object to get echonest data for, maybe it's been deleted?")
        return 
    
    print "Echonest id", echonest_id

    while True:
        response = None
        try:
            response = requests.get(
                "http://developer.echonest.com/api/v4/track/profile",
                params={"api_key": settings.ECHONEST_API_KEY, "id": echonest_id, "bucket": "audio_summary"})
            track = response.json()["response"]["track"]
        except:
            logger.error("Bad response from echonest profile: %s" % (response.text,))
            self.retry()
            
        print "Response json", response.json()
        # print "Got track"
        if track["status"] == "pending":
            # Check again in 10 seconds time
            print "Check again in 10 seconds"
            time.sleep(10)
        else:
            break
            
    print "Get track analysis"
    track_analysis = requests.get(
            track["audio_summary"]["analysis_url"]).json()
    with transaction.atomic():
        # Re-get the audio usint SELECT FOR UPDATE to avoid race conditions
        audio = models.Audio.objects.select_for_update().get(pk=audio.pk)

        audio.echonest_track_profile = track
        audio.echonest_track_analysis = track_analysis
        # print "Saving echonest data"
        audio.save()
    print "Echonest done"

    
