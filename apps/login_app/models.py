from __future__ import unicode_literals
from django.db import models
import bcrypt
import re

class UserManager(models.Manager):
    def validate_register(self, post_data):
        
        errors = []

        if len(post_data['name']) < 3:
            errors.append('Name must be longer 3 characters.')
            
        # checks db for existing user with same username
        if len(User.objects.filter(username=post_data['username'])) > 0:
            errors.append("username already in use")

        if len(post_data['password']) < 8:
            errors.append('Password cannot be less than eight characters.') 
          
        if post_data['password'] != post_data['confirm_pw']:
            errors.append('Passwords must match.')


        # after these 4 checks ***if error list is empty*** hash the pw and insert in db
        if not errors:
            # making some hash browns with salt
            hashed = bcrypt.hashpw((post_data['password'].encode()), bcrypt.gensalt(5))
            
            new_user = User.objects.create(name = post_data['name'], 
                            username = post_data['username'], 
                            password = hashed,
                            birthday = post_data['birthday'])
            print(new_user)
            return new_user
        print(errors)
        return errors

    def validate_login(self, post_data):
        # initiate error message list
        errors = [] 
        # checks for matching username in db
        if len(self.filter(username=post_data['username'])) > 0:
            
            # stores matching username into a variable named 'user'
            user = self.get(username=post_data['username'])
            print(user)
            # check to see if hashes match
            if not bcrypt.checkpw(post_data['password'].encode(), user.password.encode()):
                errors.append('username/password incorrect')
        else:
            errors.append('username/password incorrect')

        # if the
        if errors:
            return errors
        return user


class User(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    birthday = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    objects = UserManager()

    def __repr__(self):
        return "<USER object: {} {}>".format(self.name, self.username)
