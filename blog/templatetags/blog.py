# -*- coding: utf-8 -*-
from django import template

from ..models import Category

register = template.Library()

def get_category(context, limit=None):
    category = Category.objects.all()
    if limit is not None:
        category = category[0:limit]
    if category:
        context['category_list'] = category
    return context
register.inclusion_tag('blog/tag_list.html',  takes_context=True)(get_category)