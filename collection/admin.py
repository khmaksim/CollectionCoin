__author__ = 'kolobok'
from django.contrib import admin
from collection.models import Coin, Section, Metal, TypeEdge, Image, InternationalGrade, SheldonGrade, Mint


class SectionAdmin(admin.ModelAdmin):
    ordering = ['section']


class ImageInline(admin.TabularInline):
    model = Image
    extra = 2


class CoinAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'section')
    fields = (('section', 'name', 'year'), 'circulation', 'inscription', ('weight', 'diameter', 'thickness'), 'metal',
              ('type_edge', 'mint'))
    inlines = (ImageInline, )
    ordering = ('-year', 'name', )


admin.site.register(Coin, CoinAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Metal)
admin.site.register(TypeEdge)
admin.site.register(Image)
admin.site.register(InternationalGrade)
admin.site.register(SheldonGrade)
admin.site.register(Mint)
