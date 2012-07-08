# -*- coding: utf-8 -*-
from django.template.response import TemplateResponse
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from blog.models import Category, Post, Comment
from blog.forms import CommentForm

def view(request, slug):
    
    post = get_object_or_404(Post, slug=slug, visable=1)
    comments = Comment.objects.filter(post=post)
    
    form = CommentForm(request.POST or None)
    if form.is_valid():
        commentItem = form.save(commit=False)
        commentItem.post = post
        commentItem.save()
            
        messages.success(request, 'Comment added successfully')
        return HttpResponseRedirect(reverse('blog_view', args=(post.slug,))) 
        
    return TemplateResponse(request, 'blog/view.html', {'post':post, 'form':form, 'comments':comments})

def list(request, slug):
    category = get_object_or_404(Category, slug=slug)
    conditions = Q(category=category)
    
    o = request.GET.get('o')
    ob = request.GET.get('ob')
    
    if o is not None and ob is not None:

        if o == 'DESC':
            sort = '-'
        else:
            sort = ''
        
        
        sort = sort + ob
        post_list = Post.objects.filter(conditions).filter(visable=1).order_by(sort)
    else:
        post_list = Post.objects.filter(conditions).filter(visable=1)
    
    paginator = Paginator(post_list, 5) 

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except TypeError:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    return TemplateResponse(request, 'blog/list.html',{'posts':posts, 'category':category})    