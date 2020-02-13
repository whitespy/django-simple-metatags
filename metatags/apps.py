from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MetaTagsConfig(AppConfig):
    name = 'metatags'
    verbose_name = _('Meta tags')

    def ready(self):
        from . import receivers  # NOQA
