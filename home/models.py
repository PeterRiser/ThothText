from __future__ import unicode_literals
from django.db import models
from django.db.models import Max
from ckeditor.fields import RichTextField
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from custom import *
import os

def get_image_path(instance, filename):
    return os.path.join('photos', str(instance.id), filename)

 
# Create your models here.
class Textbook(models.Model):
    founder = models.CharField(max_length=256)
    title = models.CharField(max_length=256, unique=True)
    cover = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    def save(self, **kwargs):
        if Textbook.objects.filter(title=self.title).exists():
            super(Textbook,self).save(**kwargs)
        else:
            super(Textbook,self).save(**kwargs)
            t = Textbook.objects.get(title= self.title)
            newPage = Page(page_title="CoverPage", page_num=1,textbook=t)
            newPage.save()
    def __str__(self):
        return self.title
    
class Page(models.Model):

    textbook = models.ForeignKey(Textbook,related_name="pages",blank=True, null=True)
    page_title = models.CharField(max_length = 256,blank=True, null=True, unique = True)
    page_num = IntegerRangeField(min_value=0,max_value=256, blank=True, null=True)
    
    def getTextID(self):
        return self.textbook.id
        
    def __str__(self):
        return str(self.page_title)
    
    class Meta:
        ordering = ['page_num']

    def save(self, **kwargs):
        super(Page, self).save(**kwargs)
        total = Page.objects.filter(textbook = self.textbook).exclude(pk = self.pk)
        pages = total.filter(page_num__gte=self.page_num)
        if not pages:
            self.page_num = total.count()+1
        for page in pages: 
            page.page_num += 1
            page.save()
                
        
        super(Page, self).save(**kwargs)
        
        

class Section(models.Model):
    page = models.ForeignKey(Page,related_name="sections")
    section_title = models.CharField(max_length=256,null=True)
    text = RichTextField(config_name='default',null=True)
    order = models.IntegerField(default = 1)
    class Meta:
        ordering = ['order']
    def __str__(self):
        return self.section_title
        
    
    def save(self, **kwargs):
        super(Section, self).save(**kwargs)
        total = Section.objects.filter(page = self.page).exclude(pk = self.pk)
        sections = total.filter(order__gte=self.order)
        if not sections:
            self.order = total.count()+1
        for section in sections: 
            section.order += 1
            section.save()
        
                
        
        super(Section, self).save(**kwargs)
    
    def rsave(self, **kwargs):
        super(Section, self).save(**kwargs)
     