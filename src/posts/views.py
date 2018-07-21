from urllib import quote_plus  # python 2
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from comments.forms import CommentForm
from comments.models import Comment
from .forms import PostForm
from .models import Post


# Create your views here.
def home(request):
    context = {
        "title": "Home",
        "text": "Welcome to the home page.",
    }
    return render(request, "home.html", context)
    
    
def post_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404     

    form = PostForm(request.POST or None,request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request,"Successfully Created")
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "form": form,
    }
    return render(request, "form.html", context)


def post_detail(request, slug=None): 
    
    instance = get_object_or_404(Post, slug=slug)
    
    if instance.draft or instance.publish > timezone.now().date():
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404  
    query = request.GET.get("q")
    content = ''
    if query:
        content = instance.content.split(' ')
        content = [w.replace(query, '<span style="background-color: #FFFF00">%s</span>' % query) for w in content]
        instance.content = " ".join(content)
        

    initial_data = {
        "content_type": instance.get_content_type,
        "object_id": instance.id
    }
    form = CommentForm(request.POST or None, initial = initial_data)
    if form.is_valid() and request.user.is_authenticated():
        c_type = form.cleaned_data.get("content_type")
        content_type = ContentType.objects.get(model=c_type)
        obj_id = form.cleaned_data.get("object_id")
        content_data = form.cleaned_data.get("content")
        parent_obj = None
        try:
            parent_id = int(request.POST.get("parent_id"))
        except:
            parent_id = None


        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj = parent_qs.first()

                
        new_comment, created = Comment.objects.get_or_create(
                                    user = request.user,
                                    content_type = content_type,
                                    object_id = obj_id,
                                    content = content_data,
                                    parent = parent_obj,
                                )

        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())
        
        
    comments = instance.comments
    context = {
        "title": instance.title,
        "instance": instance,
        "comments": comments,
        "comment_form": form,
    }
    return render(request, "detail.html", context)


def post_list(request):
    today = timezone.now().date()
    queryset_list = Post.objects.active()
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Post.objects.all()

    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
            Q(title__icontains=query)|
            Q(content__icontains=query)|
            Q(category__icontains=query) | 
            Q(user__first_name__icontains=query)|
            Q(user__last_name__icontains=query)
            ).distinct()
    paginator = Paginator(queryset_list, 5 ) 
    page_request_var = "page"
    page = request.GET.get(page_request_var)

    try:
        queryset = paginator.page(page) 
    except PageNotAnInteger:
        queryset = paginator.page(1)

    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)
    context = {
        "object_list": queryset,
        "title": "All Posts",
        "page_request_var": page_request_var,
        "today": today,
        
    }
    return render(request, "list.html", context)


def post_update(request, slug=None):  
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None,request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        #success message
        messages.success(request, "Successfully Updated")
        return HttpResponseRedirect(instance.get_absolute_url())
 
    context = { 
        "title": instance.title, 
        "instance": instance,
        "form": form, 
    }
    return render(request, "form.html", context)


def post_delete(request, slug=None):  
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
        
    instance = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        
        instance.delete()
        messages.success(request, "Successfully Deleted")
        return redirect("post:list")
    context = {
        "instance": instance,
    }

    return render(request, "delete.html", context)
