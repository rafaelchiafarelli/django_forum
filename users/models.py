from django.db import models
from django.db.models.signals import pre_save
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from PIL import Image
from django import forms
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .Medals_and_Shileds import existing_medals, existing_badges, existing_shields, existing_conquests
import random


#given when a set of badges are received
class Shields(models.Model):
    type = models.CharField(max_length=100, 
        choices=existing_shields, 
        blank = False,
        null = False)
    def __str__(self):
        return self.type
    
#given when accomplished some task
class Badges(models.Model):
    filename = models.CharField(max_length=100, 
        choices=existing_badges['files'], 
        blank = False,
        null = False)
    type = models.CharField(max_length=100, 
        choices=existing_badges['badges'], 
        blank = False,
        null = False)
    def __str__(self):
        return self.type

#users receive this when do something to somebody 
class Medals(models.Model):
    filename = models.CharField(max_length=100, 
        choices=existing_medals['files'], 
        blank = False,
        null = False)
    type = models.CharField(max_length=100, 
        choices=existing_medals['medals'], 
        blank = False,
        null = False)
    def __str__(self):
        return self.type

#users receive this when they do something to themselves
class Conquests(models.Model):
    type = models.CharField(max_length=100, 
        choices=existing_conquests['conquests'], 
        blank = False,
        null = False)
    def __str__(self):
        return self.type
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    conquests = models.ManyToManyField(Conquests, default = None,blank = True)
    medals = models.ManyToManyField(Medals, default = None,blank = True)
    badges = models.ManyToManyField(Badges, default = None,blank = True)
    shields = models.ManyToManyField(Shields, default = None,blank = True)
    is_allowed_to_post = models.BooleanField(default = False,blank = True)
    is_activated = models.BooleanField(default = False, blank = True)
    slug = models.SlugField(unique=True, 
                            max_length=255 
                            )

    def __str__(self):
        ret = self.user.username + "Profile"
        return ret

    def save(self, force_insert=False, force_update=False, using=None):
        super().save(force_insert,force_update,using)

        img = Image.open(self.image.path)

        if img.height > 150 or img.width > 150:
            output_size = (150, 150)
            img.thumbnail(output_size)
            img.save(self.image.path)
            
    def AddBadge(self, i):
        ToAdd = Badges()
        ToAdd.type = existing_badges['badges'][i][1]
        ToAdd.filename = existing_badges['files'][i][1]
        ToAdd.save()
        self.badges.add(ToAdd)
        if self.badges.filter(type=existing_badges['badges'][i][1]).count()>=existing_badges['relation'][i][2]:
            remainder = self.badges.filter(type=i).count()%existing_badges['relation'][i][2]
            if remainder == 0:
                MedalToAdd = Medals()
                MedalToAdd.type = existing_medals['medals'][existing_badges['relation'][i][1]][1]
                MedalToAdd.filename = existing_medals['files'][existing_badges['relation'][i][1]][1]
                MedalToAdd.save()
                self.medals.add(MedalToAdd)

        
    def AddConquest(self, i):
        ToAdd = Conquests()
        ToAdd.type = existing_badges['conquests'][i][1]
        ToAdd.save()
        if self.conquests.filter(type=existing_badges['conquests'][i][1]).count()>=existing_conquests['relation'][i][2]:
            remainder = self.conquests.filter(type=i).count()%existing_conquests['relation'][i][2]
            if remainder == 0:
                ShieldToAdd = Shields()
                ShieldToAdd.type = existing_medals[existing_conquests['relation'][i][1]]
                self.medals.add(ShieldToAdd)
                self.badges.add(ToAdd)

def create_slug(instance, new_slug = None):
    ToSlug = instance.user.username + str(random.randint(55555555,99999999))
    slug = slugify(ToSlug)
    if new_slug is not None:
        slug = new_slug
    qs = Profile.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug,qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)    


pre_save.connect(pre_save_receiver, sender=Profile)

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
