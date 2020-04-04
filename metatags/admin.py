from django import forms
from django.conf import settings
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline

from .forms import MetaTagForm
from .models import MetaTag


class BaseMetaTagMeta(forms.MediaDefiningClass):

    @staticmethod
    def check_modeltranslation_app_installed():
        return 'modeltranslation' in settings.INSTALLED_APPS

    @classmethod
    def get_media_class(mcs):
        css_files = ['metatags/css/metatags.css']
        js = None
        if mcs.check_modeltranslation_app_installed():
            from modeltranslation import settings as mt_settings
            css_files.append('modeltranslation/css/tabbed_translation_fields.css')
            js = (
                'admin/js/jquery.init.js',
                'modeltranslation/js/force_jquery.js',
                mt_settings.JQUERY_UI_URL,
                'modeltranslation/js/tabbed_translation_fields.js',
            )
        return type('Media', (), {'css': {'all': css_files}, 'js': js})


class MetaTagInlineMeta(BaseMetaTagMeta):

    def __new__(mcs, name, bases, attrs):
        if mcs.check_modeltranslation_app_installed():
            from modeltranslation.admin import TranslationGenericStackedInline
            bases = (TranslationGenericStackedInline,)
        attrs['Media'] = mcs.get_media_class()
        return super().__new__(mcs, name, bases, attrs)


class MetaTagAdminMeta(BaseMetaTagMeta):

    def __new__(mcs, name, bases, attrs):
        if mcs.check_modeltranslation_app_installed():
            from modeltranslation.admin import TranslationAdmin
            bases = (TranslationAdmin,)
        attrs['Media'] = mcs.get_media_class()
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

    def get_inline_instances(self, request, obj=None):
        inlines = super().get_inline_instances(request, obj)
        if not isinstance(inlines, list):
            inlines = list(inlines)
        inlines.insert(0, MetaTagInline(self.model, self.admin_site))
        return inlines


class MetaTagAbleModelAdmin(MetaTagAbleMixin, admin.ModelAdmin):
    pass
