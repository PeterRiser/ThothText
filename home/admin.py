from django.contrib import admin
from home.models import *

# Register your models here.

from nested_inline.admin import NestedStackedInline, NestedModelAdmin
class PageAdmin(admin.ModelAdmin):
    list_display = ('page_title', 'page_num')
    list_filter = ['textbook']

class SectionAdmin(admin.ModelAdmin):
    list_display = ('section_title', 'order')
    list_filter = ['page']

admin.site.register(Section, SectionAdmin)
admin.site.register(Textbook)
admin.site.register(Page,PageAdmin)

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
    
    
