from django.db import models
from django.template import Library

from ..models import MetaTag
from ..utils import truncate_language_code_from_path, check_caching_enabled

register = Library()


@register.inclusion_tag('metatags/includes/metatags.html', takes_context=True)
def include_metatags(context, model_instance=None, default_title='', default_keywords='', default_description=''):
    is_caching_enabled = check_caching_enabled()
    meta_tags_context = {
        'title': default_title,
        'keywords': default_keywords,
        'description': default_description,
    }
    if isinstance(model_instance, models.Model):
        # Try to retrieve attached meta tags for a model instance.
        if is_caching_enabled:
            # Try fetch meta tags from cache.
            meta_tags = MetaTag.objects.fetch_from_cache_attached_to_model_instance(model_instance)
        else:
            meta_tags = MetaTag.objects.get_attached_to_model_instance(model_instance)
    else:
        # Try to retrieve meta tags by an URL-path.
        url_path = truncate_language_code_from_path(context['request'].path_info)
        if is_caching_enabled:
            meta_tags = MetaTag.objects.fetch_from_cache_attached_to_url_path(url_path)
        else:
            meta_tags = MetaTag.objects.get_attached_to_url_path(url_path)
    if meta_tags is not None:
        meta_tags_context.update((key, value) for key, value in meta_tags._asdict().items() if value)
    return {'meta_tags': meta_tags_context}
