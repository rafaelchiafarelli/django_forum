from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.template.context_processors import request
from blog.views import GetData
from . import models
from .models import Profile
from users.models import Conquests
from users.Medals_and_Shileds import existing_badges,existing_medals


def email_used(request):
    return render(request,'users/email_used.html',{})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():            
            email_from_database = User.objects.filter(email = form.cleaned_data['email'])
            print(email_from_database)
            if email_from_database.count() == 0:
                form.save()
                new_user = authenticate(username=form.cleaned_data['username'],
                                        password=form.cleaned_data['password1'],
                                        )
                current_site = get_current_site(request)
                uid = urlsafe_base64_encode(force_bytes(new_user.pk)).decode()
                token = account_activation_token.make_token(new_user)
                mail_subject = 'Ative sua conta do site Programação para Makers'
                link = '/activate/' + uid + '/' + token
                message = render_to_string('users/acc_active_email.html', {
                    'user': new_user,
                    'domain': current_site.domain,
                    'uid':uid,
                    'token':token,
                    'link':link,
                })
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(
                            mail_subject, message, to=[to_email]
                )
                email.send()
                login(request, new_user)    
                return redirect('/home/')
            else:
                return redirect('/email_used/')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required(redirect_field_name='/register/')
def profile(request,username = None):
    if username is not None:
        user = User.objects.get(username = username)
        u_form = UserUpdateForm(instance=user)
        p_form = ProfileUpdateForm(instance=user.profile)

        context = {
            'u_form': u_form,
            'p_form': p_form
        }
        context.update(GetData())
        return render(request, 'users/profile.html', context)
    
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            context =  "Seus dados foram atualizados!"
            messages.success(request,context)
            return redirect('/home/')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    context.update(GetData())
    return render(request, 'users/profile.html', context)

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()        
        user = User.objects.get(pk=uid)
        
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.is_activated = True
        user.save()
        login(request, user)
        
        return redirect('/home/')
    else:
        
        return redirect('/register/')
@login_required(redirect_field_name='/login/')
def ActivateAccount(request):
    user = User.objects.get(username = request.user.username)
    current_site = get_current_site(request)
    uid = urlsafe_base64_encode(force_bytes(user.pk)).decode()
    token = account_activation_token.make_token(user)
    mail_subject = 'Ative a sua conta do site Programação para Makers.'
    link = '/activate/' + uid + '/' + token
    message = render_to_string('users/acc_active_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid':uid,
        'token':token,
        'link':link,
    })
    to_email = user.email
    email = EmailMessage(
                mail_subject, message, to=[to_email]
    )
    email.send()
    return render(request,'users/activate_mail.html',{})



@login_required(redirect_field_name='/register/')
def victories(request):
    user = User.objects.get(username = request.user.username)
    profile = Profile.objects.get(user = user)
    medals = profile.medals.all()
    badges = profile.badges.all()
    conquests = profile.conquests.all()
    shields = profile.shields.all()

    context = { 
        'medals':medals,
        'badges':badges,
        'conquests':conquests,
        'shields':shields,
        'badge_files':existing_badges['files'],
        'medal_files':existing_medals['files'],
        }
    context.update(GetData())
    
    return render(request,'users/victories.html',context)
    
@login_required(redirect_field_name='/register/')
def share(request):
    #slug
    #facebook_link
    user = User.objects.get(username = request.user.username)
    print(user.profile.slug)
    context = {
        'slug':user.profile.slug,
        'facebook_link':'www.programacaoparamakers.com.br',
        }
    if request.method == 'POST':
        if request.POST.get("form_type") == 'ShareOnFacebook':
            #give a badge of sharing
            user.profile.AddBadge(3)
            return redirect('/home/')
            
        if request.POST.get("form_type") == "CopyToClipboard":
            #give a badge of copy to clipboard
            user.profile.AddBadge(3)
            return redirect('/home/')


    return render(request,'users/share_link.html',context)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
