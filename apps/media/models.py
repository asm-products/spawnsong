from django.db import models
from django.conf import settings
import tasks
import celery
import datetime
from storages.backends import s3boto
import uuid
from django.db import transaction
from jsonfield import JSONField

class PrivateDownloadStorage(s3boto.S3BotoStorage):
    def __init__(self, *args, **kwargs):
        kwargs.update(dict(
            acl='private',
            querystring_auth=True,
            querystring_expire=600, # 10 minutes, try to ensure people won't/can't share
            ))
        super(PrivateDownloadStorage, self).__init__(*args, **kwargs)
        
    
    def url(self, name, download_file_name=None):
        name = self._normalize_name(self._clean_name(name))
        if self.custom_domain:
            return "%s://%s/%s" % ('https' if self.secure_urls else 'http',
                                   self.custom_domain, name)
        headers = {}
        if download_file_name:
            headers["response-content-disposition"] = "attachment; filename=%s" % (download_file_name,)
        return self.connection.generate_url(self.querystring_expire,
            method='GET', bucket=self.bucket.name, key=self._encode_name(name),
            response_headers=headers,
            query_auth=self.querystring_auth, force_http=not self.secure_urls)

protected_storage = PrivateDownloadStorage()

def upload_to(prefix="uploads"):
    def get_file_path(instance, filename):
        ext = filename.split('.')[-1]
        filename = "%s.%s" % (uuid.uuid4(), ext)
        return "%s/%s" % (prefix, filename)
    return get_file_path

class Audio(models.Model):
    "An original uploaded piece of audio"
    title = models.CharField(max_length=255, blank=True, default="NO TITLE")
    created_at = models.DateTimeField(default=datetime.datetime.now)
    original = models.FileField(null=True, upload_to=upload_to("audio/original"), storage=protected_storage)
    
    echonest_track_profile = JSONField(blank=True, default=None, help_text="Data received from Echonest about the snippet, used to find the beat locations for the visualisation")
    echonest_track_analysis = JSONField(blank=True, default=None, help_text="Data received from Echonest about the snippet, used to find the beat locations for the visualisation")

    @property
    def url(self):
        return self.original.url
    
    def format_url(self, profile):
        audioformat = self.get_format(profile)
        if audioformat is None or not audioformat.state == "ready":
            return None
        return audioformat.audio_data.url

    def get_format(self, profile):
        try:
            audioformat = self.audioformat_set.get(profile=profile)
        except AudioFormat.DoesNotExist:
            return None
        return audioformat
        
    def request_echonest_data(self):
        "Kick of transcoding tasks"
        return tasks.request_echonest_data.apply_async(args=(self.id,))
        
    def transcode(self, profiles=settings.AUDIO_PROFILES_DEFAULT):
        "Kick of transcoding tasks"
        return self.transcode_subtask(profiles).delay()
    
    def transcode_subtask(self, profiles=settings.AUDIO_PROFILES_DEFAULT):
        "Create a celery subtask for transcoding and return it so that it can be included in a celery workflow"
        task_list = []
        with transaction.atomic():
            for profile_name in profiles:
                profile = settings.AUDIO_PROFILES[profile_name]
                audioformat, created = AudioFormat.objects.select_for_update().get_or_create(audio=self, profile=profile_name)
                if audioformat.state in ["initial", "failed"]:
                    task_list.append(tasks.transcode_audio.subtask(
                        args=(audioformat.id, profile),
                        link_error=tasks.transcode_audio_failed.si(audioformat.id)))
                    audioformat.state = "inprogress"
                    audioformat.save()
        return celery.group(task_list)
                    

class AudioFormat(models.Model):
    "An encoded version of a piece of audio"
    audio = models.ForeignKey(Audio)
    created_at = models.DateTimeField(default=datetime.datetime.now)
    state = models.CharField(max_length=20, choices=(("initial", "Initial"), ("inprogress","Encoding in Progress"), ("ready", "Ready (Encoded)"), ("failed", "Failed")), default="initial")
    last_error = models.CharField(max_length=255, blank=True)
    profile = models.CharField(max_length=20, choices=[(x,x) for x in settings.AUDIO_PROFILES.keys()])
    audio_data = models.FileField(null=True, upload_to=upload_to("audio/encoded"), storage=protected_storage, blank=True)

        
