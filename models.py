from django.db import models

# Create your models here.
from django.conf import settings
from django.contrib.auth.models import User




# Create your models here.

class UserProfile(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE,)
	name = models.CharField(max_length=50,default='')
	email=models.EmailField()
	username=models.CharField(max_length=50,default='')
	password=models.CharField(max_length=30)
	mobile=models.CharField(max_length=10)
   


	def _str_(self):
		return str(self.user.username)
