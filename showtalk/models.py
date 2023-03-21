from django.db import models


class user(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField('Account',max_length=20,default='',unique=True)
    password = models.CharField('Password',max_length=20, default='')
    name = models.CharField("Name",max_length=20,default='')
    img = models.ImageField(upload_to='img',default='img/images.png')
    email = models.EmailField('Email',max_length=20,default='')
    bio = models.CharField('',max_length=200,default='')
    favourite_shows = models.CharField('', max_length=200, default='')

    create_time = models.DateTimeField('create time', auto_now_add=True)
    updated_time = models.DateTimeField('updated time', auto_now=True)

    class Meta:
        db_table = 'user'
        verbose_name_plural = 'user'




class tv(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=20,default='')

    title = models.CharField(max_length=20,default='')
    docs = models.CharField('docs', max_length=200, default='')
    tv = models.FileField(upload_to='tv',default='tv/demo.mp4')

    create_time = models.DateTimeField('create time', auto_now_add=True)
    updated_time = models.DateTimeField('updated time', auto_now=True)

    class Meta:
        db_table = 'tv'

class pl(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=20,default='')
    tv_id =  models.CharField(max_length=20,default='')
    doc = models.TextField()
    create_time = models.DateTimeField('create time', auto_now_add=True)
    updated_time = models.DateTimeField('updated time', auto_now=True)

    class Meta:
        db_table = 'pl'
