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

def GetData():
    
    posts = BlogPost.objects.all()
    type = []
    for each in p_type:
        counted = BlogPost.objects.filter(type = each[0]).count()
        type += [(each[1],counted)]
    context = {
        'posts': posts,
        'post_types':type,
        'count':posts.count(),
    }
    return context


@login_required(redirect_field_name='/home/')
def home(request):
    context = {}
    context.update(GetData())
    return render(request, 'blog/home.html', context)

@login_required()
def PostDetail(request, pk):
    post = BlogPost.objects.get(id=int(pk))
    comments = BlogComment.objects.filter(post = post)
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formComment':
            comment = CommentCreateForm(request.POST)
            user = User.objects.get(username=request.user.username)        
            if comment.is_valid():
                print(int(request.POST.get('type')[0]))
                user.profile.AddBadge(0)                
                comment.author = user
                this_comment= comment.save(commit = False)
                this_comment.author = user
                this_comment.post = post
                this_comment.SendNotificationMail()
                this_comment.save()
                post.comment_count = comments.count()
                post.save()
                post = BlogPost.objects.get(id=int(pk))
        else:
            if request.POST.get("form_type") == 'formReply':
                reply = ReplyCreateForm(request.POST)
                user = User.objects.get(username=request.user.username)
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
        context.update(GetData())
    return render(request,'blog/post_detail.html',context)


@login_required()
def PostList(request, choice):
    posts = BlogPost.objects.all()
    type = []
    for each in p_type:
        counted = BlogPost.objects.filter(type = each[0]).count()
        type += [(each[1],counted)]
        if choice == each[1]:
            ListedPost = BlogPost.objects.filter(type = each[0]).order_by('-date_posted')
            this_type = each[1]
    context = {
                'ListedPost':ListedPost,
                'type':this_type,
                'post_types':type,
                'count':posts.count(),
                }
    return render(request,'blog/post_list.html',context)


class UserPostListView(ListView):
    model = BlogPost
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return BlogPost.objects.filter(author=user).order_by('-date_posted')
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

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
                this_post.save()                
                return redirect('/home/')
        else:
            return redirect('/logout/')
    else:
        form = PostCreateForm()
        context = {
                    'form':form,
                    }
        context.update(GetData())
        return render(request, 'blog/post_form.html', context)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = BlogPost
    fields = ['title', 'content', 'type', 'description','summary']

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
