from django.db import models
from django.utils.text import slugify
from django.utils.crypto import get_random_string

class Category(models.Model):
    name = models.CharField(max_length=20)
    memo = models.CharField(null=True,blank=True,max_length=255)
    slug = models.SlugField(max_length=100, unique=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:  # スラッグが未設定の場合のみ生成する
            self.slug = slugify('Cat'+ self.memo + get_random_string(length=5))            
            
        super().save(*args, **kwargs)       

class Log(models.Model):
    startDateTime = models.DateTimeField(null=True,blank=True)
    endDateTime = models.DateTimeField(null=True,blank=True)
    learnDate = models.DateField(null=True,blank=True)
    learnMinut = models.IntegerField(null=True,blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    memo = models.CharField(null=True,blank=True,max_length=255)
    slug = models.SlugField(max_length=100, unique=True) 
    
    def save(self, *args, **kwargs):
        if not self.slug:  # スラッグが未設定の場合のみ生成する
            self.slug = slugify('log'+ self.memo + get_random_string(length=5))             
            
        super().save(*args, **kwargs)       
    
   
