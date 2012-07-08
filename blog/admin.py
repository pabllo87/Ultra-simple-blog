from django.contrib import admin
from blog.models import Category, Post, Comment
from django.shortcuts import get_object_or_404
from tinymce.widgets import TinyMCE



class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug' : ('name',)}
    
class CommentInline(admin.TabularInline):
    model = Comment
    can_delete = True
    extra = 0
    
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created','category','visable',)
    prepopulated_fields = {'slug' : ('title',)}
    list_filter = ('category','visable',)
    inlines = [CommentInline,]
    
    def formfield_for_dbfield(self, db_field, **kwargs):
          if db_field.name == 'content':
              return db_field.formfield(widget=TinyMCE(
                  attrs={'cols': 80, 'rows': 30},
                #mce_attrs={},
              ))
          return super(PostAdmin, self).formfield_for_dbfield(db_field, **kwargs)
          
    actions = ['unpublish_model', 'publish_model']

    def get_actions(self, request):
        actions = super(PostAdmin, self).get_actions(request)
        return actions

    def unpublish_model(self, request, obj):
        for o in obj.all():
            o.unpublish()
    
    def publish_model(self, request, obj):
        for o in obj.all():
            o.publish()
    unpublish_model.short_description = 'Unpublish'
    publish_model.short_description = 'Publish'
    
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)