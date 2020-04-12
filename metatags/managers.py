from django.db import models

from .utils import get_object_or_none, get_cache_backend


class MetaTagQueryset(models.QuerySet):

    def attached_to_model_instance(self):
        return self.filter(content_type__isnull=False, object_id__isnull=False)

    def attached_to_url_path(self):
        return self.filter(content_type__isnull=True, object_id__isnull=True)


class MetaTagManager(models.Manager.from_queryset(MetaTagQueryset)):

    def get_attached_to_model_instance(self, model_instance):
        """
        Returns meta tags attached to a model instance.
        """
        return get_object_or_none(
            self.attached_to_model_instance(),
            content_type__app_label=model_instance._meta.app_label,
            content_type__model=model_instance._meta.model_name,
            object_id=model_instance.pk,
        )

    def get_attached_to_url_path(self, url_path):
        """
        Returns meta tags attached to an URL-path.
        """
        return get_object_or_none(self.attached_to_url_path(), url=url_path)

    def fetch_from_cache_attached_to_model_instance(self, model_instance):
        """
        Fetches attached to a model instance meta tags from cache if
        available. Otherwise tries to retrieve meta tags from a database
        and rebuilds cache.
        """
        cache = get_cache_backend()
        cache_key = self.model._compose_cache_key('{}:{}'.format(model_instance._meta.label_lower, model_instance.pk))
        # Try to get cached meta tags.
        cached_meta_tags = cache.get(cache_key)
        if cached_meta_tags is None:
            # No cached meta tags, need to rebuild.
            meta_tags = self.get_attached_to_model_instance(model_instance)
            if meta_tags is not None:
                meta_tags._rebuild_cache()
                return meta_tags
        else:
            return cached_meta_tags

    def fetch_from_cache_attached_to_url_path(self, url_path):
        """
        Fetches attached to to an URL-path meta tags from cache if
        available. Otherwise tries to retrieve meta tags from a database
        and rebuilds cache.
        """
        cache = get_cache_backend()
        cache_key = self.model._compose_cache_key(url_path)
        # Try to get cached meta tags.
        cached_meta_tags = cache.get(cache_key)
        if cached_meta_tags is None:
            # No cached meta tags, need to rebuild.
            meta_tags = self.get_attached_to_url_path(url_path)
            if meta_tags is not None:
                meta_tags._rebuild_cache()
                return meta_tags
        else:
            return cached_meta_tags
