from django.db import models

# Create your models here.


class ServerInfo(models.Model):

    def __str__(self):
        return self.friendly_name

    friendly_name = models.CharField(max_length=30)
    ae_title = models.CharField(max_length=30)
    port_num = models.IntegerField()
