from __future__ import unicode_literals
from django.db import models
from django.db.models import Max
from ckeditor.fields import RichTextField
from custom import *
import os

def get_image_path(instance, filename):
    return os.path.join('photos', str(instance.id), filename)

 
# Create your models here.
class Textbook(models.Model):
    founder = models.CharField(max_length=256)
    title = models.CharField(max_length=256)
    cover = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    def __str__(self):
        return self.title
    
class Page(models.Model):

    textbook = models.ForeignKey(Textbook,related_name="pages",blank=True, null=True)
    page_title = models.CharField(max_length = 256,blank=True, null=True)
    page_num = IntegerRangeField(min_value=0,max_value=256, blank=True, null=True)
    
    def getTextID(self):
        return self.textbook.id
        
    def __str__(self):
        return self.page_title
        
    
    def iterSave(self):
        pages = self.textbook.pages
        MAX_PAGE = pages.aggregate(Max('page_num'))
        try:
            cpy = pages.get(page_num = self.page_num)
            for page in pages:
                if page.page_num >= self.page_num:
                    obj,created = Page.objects.update_or_create(page_title = page.page_title, page_num = page.page_num+1, textbook = page.textbook)
        except:
            if self.page_num > MAX_PAGE:
                obj,created = Page.objects.update_or_create(page_title = self.page_title, page_num = self.page_num+1, textbook = self.textbook)
    
    def save(self, *args,**kwargs):
        self.iterSave()
        super(Page,self).save(*args, **kwargs)

class Section(models.Model):
    page = models.ForeignKey(Page,related_name="sections")
    section_title = models.CharField(max_length=256)
    text = RichTextField(config_name='awesome_ckeditor')
    def __str__(self):
        return self.section_title


    
        
    