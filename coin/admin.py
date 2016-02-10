__author__ = 'kolobok'

from django.contrib import admin

from .models import Coin, Section, Metal, Edge, Image


class ImageAdmin(admin.TabularInline):
    model = Image
    extra = 2


class CoinAdmin(admin.ModelAdmin):
    list_display = ('name', 'year')
    fields = ['section', 'name', 'circulation', 'inscription', 'year', 'weight', 'diameter', 'thickness', 'metal',
              'edge', 'mint']
    inlines = [ImageAdmin, ]

admin.site.register(Coin, CoinAdmin)
admin.site.register(Section)
admin.site.register(Metal)
admin.site.register(Edge)
admin.site.register(Image)