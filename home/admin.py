from django.contrib import admin

from .models import DicomServer


class ServerInfoAdmin(admin.ModelAdmin):
    list_display = ('hostname', 'ae_title', 'port')


admin.site.register(DicomServer, ServerInfoAdmin)
