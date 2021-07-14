from django.db import models

class Music(models.Model):
    # file will be uploaded to MEDIA_ROOT/before_conversion/
    file = models.FileField(upload_to='before_conversion/')
    name = models.CharField(max_length=255)
