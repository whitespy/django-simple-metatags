from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _

from .managers import MetaTagManager
from .utils import get_cache_backend, check_caching_enabled


class MetaTag(models.Model):
    url = models.CharField(_('URL-path'), max_length=100, blank=True, db_index=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey()
    title = models.CharField(_('title'), max_length=80, blank=True)
    keywords = models.CharField(_('keywords'), max_length=250, blank=True)
    description = models.TextField(_('description'), blank=True)

    objects = MetaTagManager()

    class Meta:
        ordering = ['id']
        db_table = 'metatags'
        unique_together = ['content_type', 'object_id']
        verbose_name = _('meta tags')
        verbose_name_plural = _('meta tags')

    def __str__(self):
        if self.content_object is not None:
            return force_str(self.content_object)
        return self.title

    def save(self, *args, **kwargs):
        is_inserted = not bool(self.pk)
        super().save(*args, **kwargs)
        if not is_inserted and check_caching_enabled():
            self._invalidate_cache()

    def _asdict(self):
        return {
            'title': self.title,
            'keywords': self.keywords,
            'description': self.description,
        }

    @staticmethod
    def _compose_cache_key(identifier):
        return '{cache_key_prefix}:{identifier}'.format(
            cache_key_prefix=getattr(settings, 'METATAGS_CACHE_KEY_PREFIX', 'metatags'),
            identifier=identifier,
        )

    def _get_cache_key(self):
        if self.content_object is not None:
            identifier = '{}:{}'.format(self.content_object._meta.label_lower, self.content_object.pk)
        else:
            identifier = self.url
        return self._compose_cache_key(identifier)

    def _rebuild_cache(self):
        cache = get_cache_backend()
        cache.set(
            key=self._get_cache_key(),
            value=self,
            timeout=getattr(settings, 'METATAGS_CACHE_TIMEOUT', None),
        )

    def _invalidate_cache(self):
        cache = get_cache_backend()
        cache.delete(self._get_cache_key())
