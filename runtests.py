#!/usr/bin/env python
import sys

import django
from django.conf import settings
from django.test.utils import get_runner

if __name__ == '__main__':
    test_settings = {
        'SECRET_KEY': 'test_key',
        'DATABASES': {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
            },
        },
        'CACHES': {
            'default': {
                'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            },
        },
        'INSTALLED_APPS': [
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'metatags',
        ],
    }
    settings.configure(**test_settings)
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(['metatags.tests'])
    sys.exit(bool(failures))
