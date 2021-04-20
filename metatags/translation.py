from modeltranslation.translator import TranslationOptions, translator

from .models import MetaTag


class MetaTagTranslationOptions(TranslationOptions):
    fields = ('title', 'keywords', 'description')


translator.register(MetaTag, MetaTagTranslationOptions)
