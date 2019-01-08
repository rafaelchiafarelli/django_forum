from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from blog.models import post_types as p_type
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import BlogPost, BlogComment, BlogReply
from blog.forms import PostCreateForm, CommentCreateForm, ReplyCreateForm
from django.http.response import Http404, HttpResponse
from users.Medals_and_Shileds import existing_badges, existing_conquests 
import datetime
from users.models import Profile

def GetData(request):

    posts = BlogPost.objects.all()
    type = []
    now_datetime = datetime.datetime.now() - datetime.timedelta(minutes=5)
    last_hour = BlogPost.objects.filter(date_posted__contains = now_datetime)
    embedded_news = BlogPost.objects.filter(type = 'Arduino')
    for each in p_type:
        counted = BlogPost.objects.filter(type = each[0]).count()
        type += [(each[0],counted, each[1])]
    context = {
        'posts': posts,
        'post_types':type,
        'count':posts.count(),
        'last_hour':last_hour,
        'embedded_news':embedded_news,
    }


    return context


@login_required(redirect_field_name='/home/')
def home(request, slug = None):
    if slug is not None:
        P = Profile.objects.get(slug=slug)
        if P is not None:
            P.AddConquest(1)
    context = {}
    context.update(GetData(request))
    return render(request, 'blog/home.html', context)



@login_required()
def PostDetail(request, pk,slug=None):
    if slug is not None:
        P = Profile.objects.get(slug=slug)
        if P is not None:
            P.AddConquest(1)
            
    post = BlogPost.objects.get(id=int(pk))
    comments = BlogComment.objects.filter(post = post)
    if request.method == 'POST':
        user = User.objects.get(username=request.user.username)
        if request.POST.get("form_type") == 'formComment':
            comment = CommentCreateForm(request.POST)      
            if comment.is_valid():
                
                user.profile.AddBadge(0)                
                comment.author = user
                this_comment= comment.save(commit = False)
                if this_comment.type == 2:
                    user.profile.AddConquest(3)
                if this_comment.type == 3:
                    user.profile.AddConquest(4)
                this_comment.author = user
                this_comment.post = post
                this_comment.SendNotificationMail()
                this_comment.save()
                post.comment_count = comments.count()
                post.save()
                print(post.type)
        else:
            if request.POST.get("form_type") == 'formReply':
                reply = ReplyCreateForm(request.POST)
                if request.POST.get('comment'):
                    user_comment = BlogComment.objects.get(id = request.POST.get('comment'))
                    if reply.is_valid():
                        user.profile.AddBadge(4)
                        reply.author = user
                        this_reply= reply.save(commit = False)
                        this_reply.author = user
                        this_reply.post = post
                        this_reply.comment = user_comment
                        this_reply.SendNotificationMail()
                        this_reply.save()
            else:
                if request.POST.get("form_type") == 'ShareOnFacebook':
                    user.profile.AddBadge(3)
        return redirect('/home/')
    
    else:
        reply = ReplyCreateForm()
        comment = CommentCreateForm()
        context = {
                    'post':post,
                    'comment': comment,
                    'comments':comments,
                    'reply':reply,
                    }
        context.update(GetData(request))
    return render(request,'blog/post_detail.html',context)


@login_required()
def PostList(request, username = None, choice = None):

    if choice == None:
        choice = 1
    else:
        posts = BlogPost.objects.filter(type = choice)
    if username is not None:
        user = User.objects.get(username = username)
        posts = BlogPost.objects.filter(author = user)

    context = {
                'ListedPost':posts,
                }
    context.update(GetData(request))
    return render(request,'blog/post_list.html',context)


@login_required()
def PostCreateView(request):

    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        user = User.objects.get(username=request.user.username)
        if user.profile.is_allowed_to_post is True:
            if form.is_valid():
                form.author = user
                this_post = form.save(commit = False)
                this_post.author = user      
                user.profile.AddConquest(5)          
                this_post.save()                
                return redirect('/home/')
        else:
            return redirect('/logout/')
    else:
        form = PostCreateForm()
        context = {
                    'form':form,
                    }
        context.update(GetData(request))
        return render(request, 'blog/post_form.html', context)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = BlogPost
    fields = ['title', 'content', 'type', 'description','summary']
    template_name ='blog/post_form.html'
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False



class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = BlogPost
    success_url = '/'
    template_name = 'blog/post_confirm_delete.html'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
