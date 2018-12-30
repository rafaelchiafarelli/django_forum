from django import forms
from django.db import models
from django.contrib.auth.models import User
from django.views.generic import DetailView
from tinymce import TinyMCE
from .models import EmailAdmin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .filter_types import filters


class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False


class EmailAdminCreateForm(forms.ModelForm):
    emails = models.ManyToManyField(User, default = None,blank = True)
    email_to = forms.Select(choices=filters['filters'])
    class Meta:
        model = EmailAdmin
        fields =['email_text','email_to','email_title']

