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
