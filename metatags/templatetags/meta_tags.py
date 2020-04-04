import warnings

from django.template import Library

from .metatags import include_metatags

register = Library()


@register.inclusion_tag('metatags/includes/metatags.html', takes_context=True)
def include_meta_tags(context, model_instance=None, default_title='', default_keywords='', default_description=''):
    warnings.warn(
        'The include_meta_tags template tag is deprecated in favor of '
        'include_metatags template tag and will be removed in 3.0.0 version.',
        DeprecationWarning,
        stacklevel=2,
    )
    return include_metatags(context, model_instance, default_title, default_keywords, default_description)
