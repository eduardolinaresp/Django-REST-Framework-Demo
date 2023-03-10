from django.db import models

# Create your models here.

class Article(models.Model):
      title = models.CharField(max_length=100)
      author = models.CharField(max_length=100)
      email  = models.EmailField(max_length=100)
      date   = models.DateField(auto_now=True)
      
      def __str__(self):
          return self.title
      
class Author(models.Model):
      name = models.CharField(max_length=100)
      last_name = models.CharField(max_length=100)
      country  = models.EmailField(max_length=100)
      birth_date   = models.DateField()
      
      def __str__(self):
          return self.name      