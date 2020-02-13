from collections import namedtuple

from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import MetaTag
from .templatetags.meta_tags import include_meta_tags
from .utils import truncate_language_code_from_path

UserModel = get_user_model()
HttpRequestDummy = namedtuple('HttpRequestDummy', ['path_info'])


class TestMetaTags(TestCase):

    def test_truncate_language_code_from_path(self):
        self.assertEqual(truncate_language_code_from_path('/'), '/')
        self.assertEqual(truncate_language_code_from_path('/en/'), '/')
        self.assertEqual(truncate_language_code_from_path('/end/'), '/end/')
        self.assertEqual(truncate_language_code_from_path('/en/services/'), '/services/')

    def test_retrieve_attached_meta_tags(self):
        test_user = UserModel.objects.create(username='test_user')
        meta_tags = MetaTag.objects.create(
            title='test user title',
            keywords='test user keywords',
            description='test user description',
            content_object=test_user,
        )
        meta_tags_template_context = include_meta_tags({}, test_user)['meta_tags']
        self.assertEqual(meta_tags.title, meta_tags_template_context['title'])
        self.assertEqual(meta_tags.keywords, meta_tags_template_context['keywords'])
        self.assertEqual(meta_tags.description, meta_tags_template_context['description'])

    def test_retrieve_meta_tags_by_url_path(self):
        request = HttpRequestDummy('/foo/bar/')
        meta_tags = MetaTag.objects.create(
            url='/foo/bar/',
            title='test title',
            keywords='test keywords',
            description='test description',
        )
        meta_tags_template_context = include_meta_tags({'request': request})['meta_tags']
        self.assertEqual(meta_tags.title, meta_tags_template_context['title'])
        self.assertEqual(meta_tags.keywords, meta_tags_template_context['keywords'])
        self.assertEqual(meta_tags.description, meta_tags_template_context['description'])

    def test_cascade_deletion_attached_meta_tags(self):
        test_user = UserModel.objects.create(username='test_user')
        MetaTag.objects.create(
            title='test user title',
            keywords='test user keywords',
            description='test user description',
            content_object=test_user,
        )
        self.assertTrue(MetaTag.objects.exists())
        test_user.delete()
        self.assertFalse(MetaTag.objects.exists())
