from django.db import models

# Create your models here.


class ServerInfo(models.Model):

    def __str__(self):
        return self.friendly_name

    friendly_name = models.CharField(max_length=30)
    AE_Title = models.CharField(max_length=30)
    port = models.IntegerField()
