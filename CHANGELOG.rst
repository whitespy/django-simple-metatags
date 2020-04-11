#########
Changelog
#########

Release 2.0.0
-------------

- Added caching feature
- Added database index for url field of MetaTag model
- Added MetaTagAbleMixin and MetaTagAbleModelAdmin to simplify meta tags adjusting in Django admin
- Renamed database table from meta_tags to metatags
- Removed model_title_field argument of include_meta_tags inclusion tag
- Started deprecation of meta_tags template library in favor of metatags
- Started deprecation of include_meta_tags inclusion tag in favor of include_metatags
- Fixed integration with the django-modeltranslation application

Release 1.0.1
-------------

- Added __init__.py files to management and management/commands directories to build distributive properly (issue https://github.com/pypa/setuptools/issues/97)

Release 1.0.0
-------------

- Added Django 3.0 support
- Dropped Python 2 support

Release 0.9.2 (this is the last release to support Python 2)
------------------------------------------------------------

- Added compatibility with Django 2.0
- Refactored admin forms
- Extended test suite

Release 0.9.1
-------------

- Initial release
