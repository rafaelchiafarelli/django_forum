from django import forms

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from django.views.generic import DetailView
from tinymce import TinyMCE
from .models import BlogPost, BlogComment, BlogReply
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False

class PostDetailView(DetailView,forms.ModelForm):
    model = BlogPost
    content = forms.CharField(
        widget=TinyMCEWidget(
            attrs={'required': False, 'cols': 30, 'rows': 10}
        )
    )
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields =(
            'title','content','type','summary','description'
            )
    def form_valid(self, model):
        model.instance.user = self.request.user
        return super(PostCreateForm, self).form_valid(model)

class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = BlogComment
        fields =(
            'title','content','type',
            )
    def form_valid(self, model):
        model.instance.user = self.request.user
        return super(CommentCreateForm, self).form_valid(model)
    
class ReplyCreateForm(forms.ModelForm):
    class Meta:
        model = BlogReply
        fields =(
            'title','content',
            )
    def form_valid(self, model):
        model.instance.user = self.request.user
        return super(ReplyCreateForm, self).form_valid(model)