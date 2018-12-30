from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile



class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'autocomplete': 'off',
        'class': 'form-control',
        'placeholder': 'seuemail@email.com',
        'required': 'obrigatório'
        }),error_messages={'invalid': 'email inválido, tente novamente'},required = True)

    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels    ={
                'username':'Nome de Usuário',
                'email':'Um email Válido',
                'password1':'senha',
                'password2':'repita a senha',
        }
        help_texts = {
                'username':'O nome de usuário que você vai utilizar',
                'email':'Esse deve ser seu email mais usado',
                'password1':'Escolha uma senha segura',
                'password2':'Repita a senha anterior',
        }
        error_messages={
                'username':{'required': 'Obrigatorio'},
                'email':{'required': 'Obrigatorio'},
                'password1':{'required': 'Obrigatorio'},
                'password2':{'required': 'Obrigatorio'},
                }



class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']
        help_texts = {
                'username':'Seu nome de usuário',
                'email':'Seu email de contato',
        }
        error_messages={
                'username':{'required': 'Obrigatório'},
                'email':{'required': 'Obrigatório'},
                }


TRUE_FALSE_CHOICES = (
    (True, 'Sim'),
    (False, 'Não')
)

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('image','is_allowed_to_post')
        widgets = {
            'is_allowed_to_post': forms.Select(choices=TRUE_FALSE_CHOICES)
        }





























