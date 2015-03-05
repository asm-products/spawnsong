from django.contrib import admin
import models

from sites.spawnsongsite import admin_site as site

def transcode(modeladmin, request, queryset):
    for audio in queryset:
        audio.transcode()
transcode.short_description = "Transcode to default formats"

class AudioFormatInline(admin.StackedInline):
    readonly_fields = ("state",)
    model = models.AudioFormat
    extra = 0

class AudioAdmin(admin.ModelAdmin):
    inlines = [AudioFormatInline]
    list_display = ("title", "created_at")
    date_hierarchy = "created_at"
    search_fields = ("title", "audioformat__state", "audioformat__profile")
    actions = [transcode]

site.register(models.Audio, AudioAdmin)
