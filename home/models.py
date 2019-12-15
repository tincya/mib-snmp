from django.db import models

class PCAP(models.Model):
    file_name = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')