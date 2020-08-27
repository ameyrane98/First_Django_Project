from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import (TemplateView,DetailView,ListView,CreateView,UpdateView,DeleteView)
from first_site.models import Post,Comment
from django.contrib.auth.mixins import LoginRequiredMixin
from first_site.forms import PostForm,CommentForm
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your views here.

class BaseView(TemplateView):
    template_name = 'first_site/home.html'
class AboutView(TemplateView):
    template_name = 'first_site/about.html'


class PostListView(ListView):
    model = Post


    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by("-published_date")

class PostDetailView(DetailView):
    model = Post

class CreatePostView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    redirect_field_name = 'first_site/post_detail.html'
    form_class = PostForm
    model = Post
    #### to add a photo in form## and check if photo is provided###
    # def form_valid(self,form):
    #     thumbnail = PostForm.save(commit=False)
    #     if 'image' in request.FILES:
    #         thumbnail.image = request.FILES['image']
    #     thumbnail.save()
    #     return redirect('post_detail',pk=post.pk)
class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    redirect_field_name = 'first_site/post_detail.html'
    form_class = PostForm
    model = Post
class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')

class DraftListview(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'first_site/post_list.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')

####### views for comment##########
@login_required
def post_publish(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('post_detail',pk=pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)

@login_required
def comment_approve(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    comment.approve()
    return redirect('post_detail',pk=comment.post.pk)

@login_required
def add_comment_to_post(request,pk):
    post =get_object_or_404(Post,pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail',pk=post.pk)
    else:
        form = CommentForm()
    return render(request,'first_site/comment_form.html',{'form':form})
