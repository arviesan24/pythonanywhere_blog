from django.utils.http import urlquote_plus
from django.http import HttpResponseRedirect, Http404
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone

from django.contrib.auth.decorators import login_required
from comments.forms import CommentForm
from django.contrib.contenttypes.models import ContentType
from comments.models import Comment
from django.contrib import messages
from .forms import PostForm
from .models import Post

@login_required
def post_create(request):
    #next 2 lines will only allow staff and superuser to create--remove @login_required if this will be uncommented
    # if not request.user.is_staff or not request.user.is_superuser:  #give error if not authorized user
    #     raise Http404
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request, "Story successfully added.")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "form": form,
    }
    return render(request, "post_form.html", context)

def post_detail(request, slug=None):  #retrieve
    instance = get_object_or_404(Post, slug=slug)
    if instance.draft or instance.publish > timezone.now().date():
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    share_string = urlquote_plus(instance.content)

    initial_data = {
        "content_type": instance.get_content_type,
        "object_id": instance.id,
    }
    # START OF COMMENT SECTION=====================
    form = CommentForm(request.POST or None, initial=initial_data)
    if form.is_valid() and request.user.is_authenticated():  #make sure the form is valid and user is logged in
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
            user=request.user,
            content_type=content_type,
            object_id=obj_id,
            content=content_data,
            parent=parent_obj,
        )

        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())  #clear form field after saving the content


    comments = instance.comments #Comment.objects.filter_by_instance(instance)
    #END OF COMMENT SECTION=====================


    #=============PAGINATION=============
    #Detect the breaklines from DB and split the paragraphs using it
    tempInstance = instance.content
    PaginatedInstance = tempInstance.split("\r\n\r\n")

    paginator = Paginator(PaginatedInstance, 8)  #set how many paragraph to show per page

    page = request.GET.get('page', 1)

    try:
        Paginated = paginator.page(page)
    except PageNotAnInteger:
        Paginated = paginator.page(1)
    except EmptyPage:
        Paginated = paginator.page(paginator.num_pages)

    #Post.content = Paginated

    #=========END OF PAGINATION==========

    context = {
        "title": instance.title,
        "instance": instance,
        "Paginated": Paginated,  #will use this to display the story instead of instance (divided string by paragraph)
        "share_string": share_string,
        "comments": comments,
        "comment_form": form,
        "post_creator": instance.user,
    }

    return render(request, "post_detail.html", context)

def post_list(request):  #list items
    today = timezone.now().date()
    queryset_list = Post.objects.active()  #.order_by("-timestamp")  #get all the records from models
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Post.objects.all()

    query = request.GET.get("q")  #q is for the search text value
    if query:
        queryset_list = queryset_list.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
            ).distinct()
    paginator = Paginator(queryset_list, 10)  # Show 25 queryset per page
    page_request_var = "page"
    page = request.GET.get('page')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    context = {  #save the records to a dictionary
        "object_list": queryset,  #call this object_list from the index.html to show records
        "title": "Stories",
        "page_request_var": page_request_var,
        "today": today,
    }
    return render(request, "post_list.html", context)  #call index.html and pass the data from context object

def post_update(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:  #give error if not authorized user
        raise Http404
    instance = get_object_or_404(Post, slug=slug)  #call slug from template using instance.slug
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Story successfully updated.")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "title": instance.title,
        "instance": instance,
        "form": form,
    }
    return render(request, "post_form.html", context)



def post_delete(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:  #give error if not authorized user
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    instance.delete()
    messages.success(request, "Story successfully deleted.")
    return redirect("posts:list")