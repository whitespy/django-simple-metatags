from django.template import Library
from django.utils.encoding import force_str

from ..models import MetaTag
from ..utils import get_object_or_none, truncate_language_code_from_path

register = Library()


def _get_model_instance_title(model_instance, model_title_field):
    return getattr(model_instance, model_title_field, force_str(model_instance))


@register.inclusion_tag('metatags/_meta_tags.html', takes_context=True)
def include_meta_tags(context, model_instance=None, model_title_field='title',
                      default_title='', default_keywords='', default_description=''):
    meta_tags_dict = {
        'title': default_title,
        'keywords': default_keywords,
        'description': default_description,
    }
    if model_instance is not None:
        # Try to retrieve attached meta tags for a model instance.
        meta_tags = get_object_or_none(
            klass=MetaTag,
            content_type__app_label=model_instance._meta.app_label,
            content_type__model=model_instance._meta.model_name,
            object_id=model_instance.pk,
        )
        if meta_tags is not None:
            meta_tags_dict['title'] = meta_tags.title or _get_model_instance_title(model_instance, model_title_field)
            meta_tags_dict['keywords'] = meta_tags.keywords or default_keywords
            meta_tags_dict['description'] = meta_tags.description or default_description
        else:
            meta_tags_dict['title'] = _get_model_instance_title(model_instance, model_title_field)
    else:
        # Try to retrieve meta tags by an URL-path.
        url_path = truncate_language_code_from_path(context['request'].path_info)
        meta_tags = get_object_or_none(klass=MetaTag, url=url_path)
        if meta_tags is not None:
            meta_tags_dict['title'] = meta_tags.title or default_title
            meta_tags_dict['keywords'] = meta_tags.keywords or default_keywords
            meta_tags_dict['description'] = meta_tags.description or default_description
    return {'meta_tags': meta_tags_dict}
