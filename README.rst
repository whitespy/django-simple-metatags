django-simple-metatags
======================

The django application, that allows attach title, keywords and description meta tags for
site's pages.

.. image:: https://secure.travis-ci.org/whitespy/django-simple-metatags.png
    :target: http://travis-ci.org/whitespy/django-simple-metatags

Installation
------------

.. code:: bash

    $ pip install django-simple-metatags

Configuration
-------------

1. Add 'metatags' to your INSTALLED_APPS:

.. code:: python

    INSTALLED_APPS = (
        # ...
        'metatags',
    )

2. Run migrate to create the application table:

.. code:: bash

    $ python manage.py migrate metatags

3. Include meta tags for model, add MetaTagInline in inlines of your ModelAdmin subclass
(also django-simple-metatags has the own ModelAdmin class, that allows add meta tags for URL-paths):

.. code:: python

    from metatags.admin import MetaTagInline

    class CustomModelAdmin(admin.ModelAdmin):
        # ...
        inlines = (MetaTagInline,)


4. Load meta_tags template library and create meta_tags template block in HTML head section. Add include_meta_tags
template tag in meta_tags block:

.. code:: html

    {% load meta_tags %}
    <head>
        <meta http-equiv="content-type" content="text/html; charset=utf-8" />
        {% block meta_tags %}
            {% include_meta_tags %}
        {% endblock %}
    </head>

Arguments of include_meta_tags template tag
-------------------------------------------

All arguments are optional.

**model_instance** - Model instance, to get meta tags. None by default.

**model_title_field** - Model's field, that can be used as title if meta tags title field is blank.
'title' by default.

**default_title** - Title of page by default. Used with URL-path. No sense, when the model_instance argument was passed.
'' by default.

**default_keywords** - Keywords by default.

**default_description** - Description by default.

Management command
------------------

**syncmetatags** - adds translation fields, when the django-modeltranslation application is used.
