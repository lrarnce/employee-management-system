from django.db import models
from datetime import datetime
from django.utils import timezone
from django.utils.html import mark_safe
import os, random

now = timezone.now()

# Create your models here.

class Department(models.Model):
    department_id = models.AutoField(primary_key=True)
    department_name = models.CharField(max_length=200, verbose_name='Department Name')

    def __str__(self):
        return self.department_name

    
class Position(models.Model):
    position_id = models.AutoField(primary_key=True)
    position_name = models.CharField(max_length=200, verbose_name='Position Name')

    def __str__(self):
        return self.position_name
    

def image_path(instance, filename):
    base_filename, file_extension = os.path.splitext(filename)
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWYZ1234567890'
    random_str = ''.join((random.choice(chars)for x in range(10)))
    date_now = datetime.now()
    
    return 'user_image/{year}-{month}-{day}-{base_filename}-{random_str}{file_extension}'.format(
        year = date_now.strftime('%Y'),
        month = date_now.strftime('%m'),
        day = date_now.strftime('%d'),
        
        base_filename=base_filename,
        random_str = random_str,
        file_extension = file_extension
    )
class User(models.Model):
    user_fname = models.CharField(max_length=200, verbose_name='First Name')
    user_lname = models.CharField(max_length=200, verbose_name='Last Name')
    user_email = models.EmailField(unique=True, max_length=200, verbose_name='Email')
    user_department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name='Department')
    user_position = models.ForeignKey(Position, on_delete=models.CASCADE, verbose_name = 'Position')
    user_image = models.ImageField(upload_to=image_path, default='user_image/user_default_image.jpg')
    user_date_added = models.DateField(default=now)

    def image_tag(self):
        return mark_safe('<img src="/users%s" width="50" height="50"/>'%(self.user_image.url))
    

    def __str__(self):
        return self.user_email

