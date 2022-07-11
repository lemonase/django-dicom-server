from django.contrib import admin

from .models import DicomServer


class ServerInfoAdmin(admin.ModelAdmin):
    list_display = ('hostname', 'ae_title', 'ip_address', 'port', 'is_running')


admin.site.register(DicomServer, ServerInfoAdmin)
