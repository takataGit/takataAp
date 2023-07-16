from django.db import models
from django.utils.text import slugify
from django.utils.crypto import get_random_string

class Category(models.Model):
    name = models.CharField(max_length=20)
    memo = models.CharField(null=True,blank=True,max_length=255)
    slug = models.SlugField(max_length=100, unique=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:  # スラッグが未設定の場合のみ生成する
            self.slug = slugify('Cat'+ self.name) 
        if Log.objects.filter(slug=self.slug).exists():
            # すでに同じスラッグが存在する場合は、一意なスラッグを生成する
            random_string = get_random_string(length=5)  # 5文字のランダム文字列を生成
            self.slug = f"{self.slug}-{random_string}"             
            
        super().save(*args, **kwargs)       

class Log(models.Model):
    startDateTime = models.DateTimeField(null=True,blank=True)
    endDateTime = models.DateTimeField(null=True,blank=True)
    learnMinut = models.IntegerField(null=True,blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    memo = models.CharField(null=True,blank=True,max_length=255)
    slug = models.SlugField(max_length=100, unique=True) 
    
    def save(self, *args, **kwargs):
        if not self.slug:  # スラッグが未設定の場合のみ生成する
            self.slug = slugify('log'+ self.memo) 
        if Log.objects.filter(slug=self.slug).exists():
            # すでに同じスラッグが存在する場合は、一意なスラッグを生成する
            random_string = get_random_string(length=5)  # 5文字のランダム文字列を生成
            self.slug = f"{self.slug}-{random_string}"             
            
        super().save(*args, **kwargs)
    
   
