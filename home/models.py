from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Textbook(models.Model):
    founder = models.CharField(max_length=256)
    title = models.CharField(max_length=256)
    
class Page(models.Model):
    textbook = models.ForeignKey(Textbook,related_name="pages")
    page_title = models.CharField(max_length = 256)
    def __str__(self):
        return self.page_title

class Section(models.Model):
    page = models.ForeignKey
    section_title = models.CharField(max_length=256)
    text = models.CharField(max_length = 1024)
    image = models.CharField(max_length = 256)
