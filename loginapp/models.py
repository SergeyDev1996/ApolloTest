from django.db import models


class RequestData(models.Model):
    url = models.URLField(max_length=256, blank=False, null=False)
    headers = models.CharField(max_length=3000, blank=False, null=False)
    payload = models.CharField(max_length=256, blank=False, null=False)
    cookies = models.CharField(max_length=3000, blank=False, null=False)
