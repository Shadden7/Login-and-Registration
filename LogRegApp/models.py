import email
from django.db import models
import re

class UserManager(models.Manager):
    def validator(self,postData):
            errors = {}
            EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
            emails=Users.objects.filter(email=postData['email'])
            if len(emails)>0:
                errors['emailExist']="This Email is already in use"
                return errors
            if len(postData['fname'])<2:
                errors['fname']=" First name should be more than 2 characters"
            if len(postData['lname'])<2:
                errors['lname']=" Last name should be more than 2 characters"   
            if not EMAIL_REGEX.match(postData['email']):                
                errors['email'] = "Invalid email address!"   
            if len(postData['password'])<8:
                errors['password']=" Password should be at least 8 characters"      
            if not postData['password'] == postData['cpw']:
                errors['cpw']='password and confirm password must be tha same'
            return errors
    
   # def login_validator(self,postData):
    #    errors = {}
     #       EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
      #      if not EMAIL_REGEX.match(postData['email']):                
       #         errors['email'] = "Invalid email address!"
        


# Create your models here.
class Users(models.Model):
    fname=models.CharField(max_length=255)
    lname=models.CharField(max_length=255)
    email=models.EmailField(max_length=255)
    password=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects= UserManager()

    
