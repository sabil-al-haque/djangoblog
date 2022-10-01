from django.db import models

# Create your models here.
class Post(models.Model):
 title = models.CharField(max_length=150)
 desc = models.TextField()



 # Create your contact models here.
class Contact(models.Model):
 name = models.CharField(max_length=150)
 email = models.EmailField()
 phone = models.CharField(max_length=150)
 comment= models.TextField()


 def __str__(self):
     return 'Message from ' + self.name
