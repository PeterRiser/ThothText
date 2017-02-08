from django.contrib import admin
from home.models import *

# Register your models here.

from nested_inline.admin import NestedStackedInline, NestedModelAdmin

admin.site.register(Section)
admin.site.register(Textbook)
admin.site.register(Page)

# '''
# class SectionInline(NestedStackedInline):
#     model = Section
#     extra = 1


# class PageInline(NestedStackedInline):
#     model = Page
#     extra = 1
#     inlines = [SectionInline]


# @admin.register(Textbook)
# class TextbookAdmin(NestedModelAdmin):
#     inlines = [PageInline]
# '''
    
    
