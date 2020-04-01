import warnings

from django.template import Library

from .metatags import include_metatags

warnings.warn(
    'The meta_tags template module is deprecated and will be removed '
    'in 3.0.0 in favor of metatags module.',
    DeprecationWarning,
)
register = Library()


@register.inclusion_tag('metatags/includes/metatags.html', takes_context=True)
def include_meta_tags(context, model_instance=None, default_title='', default_keywords='', default_description=''):
    warnings.warn(
        'The include_meta_tags template tag is deprecated and will be removed '
        'in 3.0.0 in favor of include_metatags template tag.',
        DeprecationWarning,
    )
    return include_metatags(context, model_instance, default_title, default_keywords, default_description)
