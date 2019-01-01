from django.shortcuts import render, get_object_or_404, redirect

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.conf import settings

from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import EmailAdmin
from blog.views import GetData
from .forms import EmailAdminCreateForm
from users.models import Profile

@login_required()
def EmailSentView(request):
    Email = EmailAdmin.objects.all()
    context = {
                'email_list':Email,
                }
    context.update(GetData(request))
    return render(request,'EmailAdmin/EmailAdmin_list.html',context)


@login_required()
def EmailLandPage(request):

    context = GetData(request)
    return render(request,'EmailAdmin/EmailAdmin_LandPage.html',context)


@login_required()
def EmailSentDetail(request, pk):
    Email = EmailAdmin.objects.get(id=int(pk))
    
    dest = Email.emails.all()


    print(dest)
    context ={
        'email':Email,
        'email_to':dest,
        }
    context.update(GetData(request))
    return render(request,'EmailAdmin/EmailAdmin_detail.html',context)

@login_required()
def EmailToSendCreation(request):

    
    if request.method == 'POST':
        form = EmailAdminCreateForm(request.POST)
        user = User.objects.get(username=request.user.username)
        if user.profile.is_allowed_to_post is True and user.is_staff is True:
            print("is allowed to post and is staff")
            if form.is_valid():
                print("is valid")
                
                #send email to all or schedule a email send and save the message
                if request.POST.get('email_to') == '0':
                    profiles = Profile.objects.filter(is_activated = True)
                    ToSave = form.save(commit = False)
                    for profile in profiles:
                        usr = User.objects.get(profile = profile)
                        message = render_to_string('EmailAdmin/EmailAdmin_send.html', {
                            'user': usr,
                            'message': ToSave,
                        })
                        plain_message = strip_tags(message)
                        mail.send_mail(ToSave.email_title, plain_message,from_email= settings.EMAIL_HOST_USER,recipient_list=[usr.email], html_message=message)
                        ToSave.save()
                        ToSave.emails.add(usr)
                        print(usr)
                    
                
                if request.POST.get('email_to') == '1':
                    profiles = Profile.objects.filter(is_activated = False)
                    ToSave = form.save(commit = False)
                    for profile in profiles:
                        usr = User.objects.get(profile = profile)
                        message = render_to_string('EmailAdmin/EmailAdmin_send.html', {
                            'user': usr,
                            'message': ToSave,
                        })
                        plain_message = strip_tags(message)
                        mail.send_mail(ToSave.email_title, plain_message,from_email= settings.EMAIL_HOST_USER,recipient_list=[usr.email], html_message=message)
                        ToSave.save()
                        ToSave.emails.add(usr)
                        print(usr)

                if request.POST.get('email_to') == '2':
                    profiles = Profile.objects.filter(is_allowed_to_post = True)
                    ToSave = form.save(commit = False)
                    for profile in profiles:
                        usr = User.objects.get(profile = profile)
                        message = render_to_string('EmailAdmin/EmailAdmin_send.html', {
                            'user': usr,
                            'message': ToSave,
                        })
                        plain_message = strip_tags(message)
                        mail.send_mail(ToSave.email_title, plain_message,from_email= settings.EMAIL_HOST_USER,recipient_list=[usr.email], html_message=message)
                        ToSave.save()
                        ToSave.emails.add(usr)
                        print(usr)
                    
                        
                if request.POST.get('email_to') == '3':
                    profiles = Profile.objects.filter(is_allowed_to_post = False)
                    ToSave = form.save(commit = False)
                    for profile in profiles:
                        usr = User.objects.get(profile = profile)
                        message = render_to_string('EmailAdmin/EmailAdmin_send.html', {
                            'user': usr,
                            'message': ToSave,
                        })
                        plain_message = strip_tags(message)
                        mail.send_mail(ToSave.email_title, plain_message,from_email= settings.EMAIL_HOST_USER,recipient_list=[usr.email], html_message=message)
                        ToSave.save()
                        ToSave.emails.add(usr)
                        print(usr)
                    
                        
                if request.POST.get('email_to') == '4':
                    form.emails = User.objects.all()
                    ToSave = form.save(commit = False)
                    for usr in form.emails:
                        message = render_to_string('EmailAdmin/EmailAdmin_send.html', {
                            'user': usr,
                            'message': ToSave,
                        })
                        plain_message = strip_tags(message)
                        mail.send_mail(ToSave.email_title, plain_message,from_email= settings.EMAIL_HOST_USER,recipient_list=[usr.email], html_message=message)
                        print(usr)
                    form.save()
 
                    
                
                return redirect('/EmailAdmin/list/')
        else:
            return redirect('/logout/')
    else:
        form = EmailAdminCreateForm()
        context = {
                    'form':form,
                    }
        context.update(GetData(request))
        return render(request, 'EmailAdmin/EmailAdmin_create.html', context)
