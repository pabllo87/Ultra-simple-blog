# -*- coding: utf-8 -*-
from django.db import models
import datetime
from lib.UniqueSlug import SlugifyUniquely

class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Name")
    slug = models.CharField(max_length=255, verbose_name="URL", unique=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        
    def __str__(self):
            return self.name
        
    def __unicode__(self):
            return self.name
    
class Post(models.Model):
    category = models.ForeignKey(Category, verbose_name="Category")
    title = models.CharField(max_length=255, verbose_name="Title")
    slug = models.CharField(max_length=255, verbose_name="URL", unique=True)
    content = models.TextField(blank=True, null=True, verbose_name="Content")
    visable = models.BooleanField(verbose_name="Visable", help_text="Whether the entry will be visible on the site.")
    created = models.DateTimeField(auto_now_add=True, editable=False)
    
    def save(self):
        if not self.id:
            # replace self.name with your prepopulate_from field
            self.slug = SlugifyUniquely(self.title, self.__class__)
        super(self.__class__, self).save()
    
    class Meta:
        ordering = ['-created']
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        
    def __str__(self):
        return self.title
    def __unicode__(self):
        return self.title

    def unpublish(self, *args, **kwargs):
        self.visable = False
        self.save()
        
    def publish(self, *args, **kwargs):
        self.visable = True
        self.save()
    
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="post_comment", verbose_name='Post')
    name = models.CharField(max_length=255, verbose_name="Name")
    content = models.TextField(verbose_name='Content')
    created = models.DateTimeField(auto_now_add=True, editable=False)
    
    class Meta:
        ordering = ['-created']
        verbose_name='Comment'
        verbose_name_plural='Comments'
    
    def __str__(self):
        return self.content
    def __unicode__(self):
        return self.content