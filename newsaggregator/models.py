from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Categories(models.Model):
    name = models.CharField(max_length=64)

    def __str__(c):
        return c.name

class UsersList(models.Model):
    username  = models.CharField(max_length=64)
    categories = models.ManyToManyField(Categories,blank=True,related_name="categories")

class savedNews(models.Model):
    username  = models.CharField(max_length=64)
    link = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    category = models.CharField(max_length=64)
