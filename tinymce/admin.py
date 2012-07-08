# -*- coding: utf-8 -*-
from django import forms
from django.core.urlresolvers import reverse
from flatpages.admin import FlatPageAdmin
from flatpages.models import FlatPage
from tinymce.widgets import TinyMCE
from django.contrib import admin

class TinyMCEFlatPageAdmin(FlatPageAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'content':
            return db_field.formfield(widget=TinyMCE(
                attrs={'cols': 80, 'rows': 30},
            ))
        return super(TinyMCEFlatPageAdmin, self).formfield_for_dbfield(db_field, **kwargs)

admin.site.unregister(FlatPage)
admin.site.register(FlatPage, TinyMCEFlatPageAdmin)