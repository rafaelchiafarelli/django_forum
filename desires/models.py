from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from tinymce import HTMLField
from blog.post_types import post_types
from django.template.loader import render_to_string
from django.core.mail import EmailMessage


class UserDesire(models.Model):
    title = models.CharField(max_length=100)
    content = HTMLField('Content')
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank = False, null = False)
    type = models.CharField(max_length=100, 
        choices=post_types, 
        default = 'Miscelanea',
        blank = False,
        null = True)
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    
    
    
    
    
    
    
    
 