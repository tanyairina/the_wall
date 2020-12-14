from django.db import models
from datetime import datetime
import re
import bcrypt

class UserManager(models.Manager):
    def basic_validator(self, postdata):
        errors = {}
        if len(postdata['fname']) < 2: 
            errors['fname'] = "Your first name must be at least 2 characters"
        if len(postdata['lname']) < 2:
            errors['lname'] = "Your last name must be at least 2 characters"
        if len(postdata['password']) < 8:
            errors['password'] = "Your password must be at least 8 characters"
        email_checker = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not email_checker.match(postdata['email']):
            errors['email'] = 'Email must be valid'
        if postdata['password'] != postdata['confpw']:
            errors['password'] = 'Password and Confirm Password do not match'
        if int(postdata['age']) < 13:
            errors['age'] = "Your must be 13 yrs old at least"
        if datetime.strptime(postdata['birth_date'], '%Y-%m-%d') > datetime.now():
            errors['birth_date'] = "Enter correct birthday, date should be in the past"
        email_check = self.filter(email=postdata['email'])
        if email_check:
            errors['email'] = "Email already in use"
        if postdata['password'] != postdata['confpw']:
            errors['password'] = 'Password and Confirm Password do not match'
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    birth_date = models.DateField(null=True)
    age = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    
    objects = UserManager()

class Wall_Message(models.Model):
    message = models.CharField(max_length=255)
    poster = models.ForeignKey(User, related_name='wall_messages', on_delete=models.CASCADE)
    user_likes = models.ManyToManyField(User, related_name='liked_posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)   

class Comment(models.Model):
    comment = models.CharField(max_length=255)
    poster = models.ForeignKey(User, related_name='wall_comments', on_delete=models.CASCADE)
    wall_message = models.ForeignKey(Wall_Message, related_name="post_comments", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)   

