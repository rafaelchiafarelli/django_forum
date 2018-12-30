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
from blog.views import GetData
from .models import UserDesire
from .forms import DesireCreateForm, DesireViewForm
from django.http.response import Http404, HttpResponse

#all the users desires
def DesireListView(request):
    desires = UserDesire.objects.all()
    context = {
                'desires':desires,
               }
    context.update(GetData())
    return render(request,'desires/desire_list.html',context)
    
@login_required()
def DesireList(request, username = None):
    if username is not None:
        author = User.objects.get(username = username)
        desires = UserDesire.objects.filter(author = author)
        context = {
                    'desires':desires,
                    }
        context.update(GetData())
        return render(request,'desires/desire_list.html',context)
    
    desires = UserDesire.objects.filter(author = request.user)
    context = {
                'desires':desires,
                }
    context.update(GetData())
    return render(request,'desires/desire_list.html',context)

@login_required()
def DesireDetail(request, pk):
    desire = UserDesire.objects.get(id=int(pk))
    context ={
        'desire':desire,
        }
    context.update(GetData())
    return render(request,'desires/desire_detail.html',context)

@login_required()
def DesireCreateView(request):
    if request.method == 'POST':
        form = DesireCreateForm(request.POST)
        user = User.objects.get(username=request.user.username)
        if form.is_valid():
            form.author = user
            desire = form.save(commit = False)
            desire.author = user                
            desire.save()                
            user.profile.AddBadge(2)
            return redirect('/desire/user/list/')

    else:
        form = DesireCreateForm()
        context = {
                    'form':form,
                    }
        context.update(GetData())
        return render(request, 'desires/desire_create.html', context)

class DesireUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = UserDesire
    template_name = 'desires/desire_update.html'  # <app>/<model>_<viewtype>.html
    fields = ['title', 'content', 'type']
    success_url = '/desire/'
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        desire = self.get_object()
        if self.request.user == desire.author:
            return True
        return False
    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)
        context.update(GetData())
        return context 

class DesireDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = UserDesire
    success_url = '/'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


