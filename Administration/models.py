from django.db import models
from tinymce import HTMLField
from django.urls import reverse
from django.utils import timezone
from .filter_types import filters
from django.contrib.auth.models import User

# Create your models here.

# send email to all users about launch a product
# send email to all users about updates in the system
# send email to all users about downtime
# send email to all users about post from adminm

#give access to the database admin page{
#add/delete/change data in the database
#}




class EmailAdmin(models.Model):
    email_text = HTMLField('Content')
    email_title = models.CharField(max_length = 100)
    emails = models.ManyToManyField(User, default = None,blank = True)
    email_to = models.CharField(max_length=100, 
        choices=filters['filters'], 
        default = 4,
        blank = False,
        null = False)
    date_and_time = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.email_text
    def get_absolute_url(self):
        return reverse('email-detail', kwargs = {'pk':self.pk})