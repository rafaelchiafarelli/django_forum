from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from tinymce import HTMLField
from .post_types import post_types, comment_types
from django.template.loader import render_to_string
from django.core.mail import EmailMessage


class BlogPost(models.Model):
    title = models.CharField(max_length=100)
    content = HTMLField('Content')
    summary = HTMLField('Summary', blank = True, null = True)
    description = HTMLField('Description')
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank = False, null = False)
    type = models.CharField(max_length=100, 
        choices=post_types, 
        default = 'Miscelanea',
        blank = False,
        null = True)
    comment_count = models.PositiveIntegerField(blank = True,default = 0)
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


class BlogComment(models.Model):
    title = models.CharField(max_length=100,blank = True, null = True)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank = False, null = False)
    post = models.ForeignKey(BlogPost,on_delete=models.CASCADE)
    type = models.CharField(max_length=100, 
        choices=comment_types, 
        default = 'Comentário Comum',
        blank = False,
        null = True)
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('comment-detail', kwargs={'pk': self.pk})
    
    def SendNotificationMail(self):
        #send notifications to all envolved
        #send notification to the post ownder, to the comment owner and to the reply owner
        
        mail_subject = 'Comentário no site Programação para Makers'
        message = render_to_string('blog/comment_notification_mail.html', {
            'comment':self,
            'post':self.post,
        })
        to_email = [
            self.author.email,
            self.post.author.email,
            ]
        email = EmailMessage(
                mail_subject, 
                message, 
                to=to_email
        )
        email.send()
        
        
class BlogReply(models.Model):
    title = models.CharField(max_length=100,blank = True, null = True)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank = False, null = False)
    comment = models.ForeignKey(BlogComment,on_delete=models.CASCADE)
    post = models.ForeignKey(BlogPost,on_delete=models.CASCADE, blank = True)
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('reply-detail', kwargs={'pk': self.pk})
    
    def SendNotificationMail(self):
        #send notifications to all envolved
        #send notification to the post ownder, to the comment owner and to the reply owner
        
        mail_subject = 'Resposta ao comentário no Site Programação para Makers'
        message = render_to_string('blog/reply_notification_mail.html', {
            'reply':self,
            'comment':self.comment,
            'post':self.post,
            
        })
        to_email = [
            self.author.email,
            self.post.author.email,
            self.comment.author.email,
            ]
        email = EmailMessage(
                mail_subject, 
                message, 
                to=to_email
        )
        email.send()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
 