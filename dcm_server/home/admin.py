from django.contrib import admin

from .models import ServerInfo


class ServerInfoAdmin(admin.ModelAdmin):
    list_display = ('friendly_name', 'AE_Title', 'port')


admin.site.register(ServerInfo, ServerInfoAdmin)
