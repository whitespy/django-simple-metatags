from django.conf import settings
from django.core.cache import caches, InvalidCacheBackendError, DEFAULT_CACHE_ALIAS
from django.shortcuts import _get_queryset
from django.utils.translation import get_language_from_path


def truncate_language_code_from_path(path):
    """
    Truncates language code from URL-path.
    """
    language_code = get_language_from_path(path)
    if language_code:
        return path.replace('/{}'.format(language_code), '', 1) or '/'
    return path


def get_object_or_none(klass, *args, **kwargs):
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        return None


def get_cache_backend():
    """
    Returns cache backend instance. Raises InvalidCacheBackendError if cache
    backend is not configured.
    """
    cache_alias = getattr(settings, 'METATAGS_CACHE_ALIAS', DEFAULT_CACHE_ALIAS)
    return caches[cache_alias]


def check_caching_enabled():
    """
    Returns True if cache backend configured and meta tags caching enabled.
    False otherwise.
    """
    try:
        get_cache_backend()
    except InvalidCacheBackendError:
        return False
    return getattr(settings, 'METATAGS_CACHE_ENABLED', False)


def reset_meta_tags_cache():
    cache = get_cache_backend()
    meta_tags_cache_keys = cache.keys('{}:*'.format(getattr(settings, 'METATAGS_CACHE_KEY_PREFIX', 'metatags')))
    if meta_tags_cache_keys:
        cache.delete_many(meta_tags_cache_keys)
