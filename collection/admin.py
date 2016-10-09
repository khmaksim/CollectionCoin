from django.contrib import admin
from collection.models import Coin, Section, Metal, TypeEdge, Image, InternationalGrade, SheldonGrade, Mint


class SectionAdmin(admin.ModelAdmin):
    ordering = ['name']
    list_display = ('name', 'parent_section')


class ImageInline(admin.TabularInline):
    model = Image
    max_num = 2
    extra = 2


class SectionFilter(admin.SimpleListFilter):
    title = u'Раздел'
    parameter_name = 'section'

    def lookups(self, request, model_admin):
        # sections = set([coin.section for coin in model_admin.model.objects.all()])
        sections = Section.objects.all()
        return [(s.id, s.name) for s in sections]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(section__id__in=self.get_children_sections(self.value()))
        else:
            return queryset

    def get_children_sections(self, value):
        sections = Section.objects.filter(parent_section__exact=value)
        if not sections.exists():
            return [value]
        sec = []
        for s in sections:
            sec.extend(self.get_children_sections(s.id))
        print(sec)
        return sec


class CoinAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'section')
    fieldsets = (
        (None, {
            'fields': (('section', 'name', 'year'),  'metal')
        }),
        ('Advanced', {
            'classes': ('collapse',),
            'fields': ('circulation', 'inscription', ('weight', 'diameter', 'thickness'), 'type_edge', 'mint'),
        }),
    )
    list_filter = (SectionFilter,)
    inlines = [ImageInline, ]
    ordering = ('-year', 'name',)
    filter_horizontal = ['metal']
    radio_fields = {'type_edge': admin.HORIZONTAL, 'mint': admin.HORIZONTAL}
    save_on_top = True
    search_fields = ['name']


admin.site.register(Coin, CoinAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Metal)
admin.site.register(TypeEdge)
admin.site.register(Image)
admin.site.register(InternationalGrade)
admin.site.register(SheldonGrade)
admin.site.register(Mint)
