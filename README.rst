======================
django-simple-metatags
======================

.. image:: https://secure.travis-ci.org/whitespy/django-simple-metatags.svg
    :target: http://travis-ci.org/whitespy/django-simple-metatags

.. image:: https://badge.fury.io/py/django-simple-metatags.svg
    :target: https://badge.fury.io/py/django-simple-metatags

.. image:: https://codecov.io/gh/whitespy/django-simple-metatags/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/whitespy/django-simple-metatags

.. image:: https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336
    :target: https://pycqa.github.io/isort/

|

The django application allows to add title, keywords and description meta tags to site's pages.

Features
--------

- Attaching meta tags to model instances
- Attaching meta tags to URL paths
- Caching
- Integration with the django-modeltranslation application

Installation
------------

.. code:: bash

    pip install django-simple-metatags

Configuration
-------------

1. Add 'metatags' to your INSTALLED_APPS:

.. code:: python

    INSTALLED_APPS = (
        # ...
        'metatags',
    )

2. Run the migrate management command:

.. code:: bash

    python manage.py migrate metatags

3. Customize model admin classes:

To be able to attach meta tags to a model instance you should slightly adjust a model admin class.

The first way by adding the **MetaTagInline** class in inlines sequence:

.. code:: python

    from metatags.admin import MetaTagInline


    class CustomModelAdmin(admin.ModelAdmin):
        # ...
        inlines = (MetaTagInline,)

The second way by using **MetaTagAbleMixin**:

.. code:: python

    from metatags.admin import MetaTagAbleMixin


    class CustomModelAdmin(MetaTagAbleMixin, admin.ModelAdmin):
        # ...

The third and way by using **MetaTagAbleModelAdmin**:

.. code:: python

    from metatags.admin import MetaTagAbleModelAdmin


    class CustomModelAdmin(MetaTagAbleModelAdmin):
        # ...

.. warning::

    Meta tags can be attached only to models that has auto-incrementing or positive integer primary key.

.. note::

    Also django-simple-metatags application has an own model admin class that allows to attach meta tags to URL
    paths.

4. Load the metatags template library and add the include_metatags template tag in template.

Add the include_metatags template tag with the model_instance argument to use meta tags attached to a model instance.

.. code:: html

    {% load metatags %}
    <head>
        <meta http-equiv="content-type" content="text/html; charset=utf-8" />
        {% include_metatags object default_title='Foo' default_keywords='Foo, bar, baz' %}
    </head>

.. note::

    The model_instance attribute is just an instance of arbitrary model like User, FlatPage, etc. with attached via
    Django's admin meta tags. A variable than contains a model instance must be included in the template context.

Add the include_metatags without the model_instance argument to use meta tags attached to an URL path.

.. code:: html

    {% load metatags %}
    <head>
        <meta http-equiv="content-type" content="text/html; charset=utf-8" />
        {% include_metatags default_title='Foo' default_keywords='Foo, bar, baz' %}
    </head>

Arguments of include_metatags template tag
------------------------------------------

All arguments are optional.

**model_instance** - A model instance with attached meta tags. Defaults to **None**.

**default_title** - A default title of page. Defaults to **''**.

**default_keywords** - Default keywords of page. Defaults to **''**.

**default_description** - Default description of page. Defaults to **''**.

Caching
-------

Since version 2.0.0 application gained caching support. See settings section for more details.

Settings
--------

**METATAGS_CACHE_ENABLED** - Enables meta tags caching to minimize database access. Defaults to **False**.

.. note::

    Django's caching system must be configured.

**METATAGS_CACHE_ALIAS** - A name of cache backend used by meta tags caching feature. Defaults to **default**.

**METATAGS_CACHE_TIMEOUT** - Timeout in seconds to use for meta tags caching. If value set up to **None**
cached meta tags never expire. Defaults to **None**.

.. note::

    Value of **0** causes meta tags to immediately expire.

Management command
------------------

**resetmetatagscache** - Removes all cached meta tags.
