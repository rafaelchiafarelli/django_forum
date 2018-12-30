from django import forms

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from django.views.generic import DetailView
from tinymce import TinyMCE
from .models import UserDesire
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False

class DesireViewForm(DetailView,forms.ModelForm):
    model = UserDesire
    content = forms.CharField(
        widget=TinyMCEWidget(
            attrs={'required': False, 'cols': 30, 'rows': 10}
        )
    )
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class DesireCreateForm(forms.ModelForm):
    class Meta:
        model = UserDesire
        fields =(
            'title','type','content',
            )
    def form_valid(self, model):
        model.instance.user = self.request.user
        return super(DesireCreateForm, self).form_valid(model)

