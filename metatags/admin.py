from django import forms
from django.conf import settings
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline

from .forms import MetaTagForm
from .models import MetaTag
from .utils import get_media_class


class MetaTagInlineMeta(forms.MediaDefiningClass):

    def __new__(mcs, name, bases, attrs):
        if 'modeltranslation' in settings.INSTALLED_APPS:
            from modeltranslation.admin import TranslationGenericStackedInline
            bases = (TranslationGenericStackedInline,)
            attrs['Media'] = get_media_class()
        return super().__new__(mcs, name, bases, attrs)


class MetaTagAdminMeta(forms.MediaDefiningClass):

    def __new__(mcs, name, bases, attrs):
        if 'modeltranslation' in settings.INSTALLED_APPS:
            from modeltranslation.admin import TranslationAdmin
            bases = (TranslationAdmin,)
            attrs['Media'] = get_media_class()
        return super().__new__(mcs, name, bases, attrs)


class MetaTagInline(GenericStackedInline, metaclass=MetaTagInlineMeta):
    model = MetaTag
    extra = 1
    max_num = 1
    can_delete = False
    fields = ('title', 'keywords', 'description')
    template = 'metatags/admin/edit_inline/stacked.html'


@admin.register(MetaTag)
class MetaTagAdmin(admin.ModelAdmin, metaclass=MetaTagAdminMeta):
    form = MetaTagForm
    list_display = list_display_links = ('url', 'title')
    search_fields = ('url', 'title', 'keywords', 'description')

    def get_queryset(self, request):
        return super().get_queryset(request).attached_to_url_path()


class MetaTagAbleMixin:

    def get_inlines(self, request, ob):
        inlines = super().get_inlines(request, ob)
        inlines = inlines + (MetaTagInline,)
        return inlines


class MetaTagAbleModelAdmin(MetaTagAbleMixin, admin.ModelAdmin):
    pass
