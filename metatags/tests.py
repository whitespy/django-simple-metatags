from collections import namedtuple

from django.contrib.auth import get_user_model
from django.test import SimpleTestCase, TestCase, override_settings

from .models import MetaTag
from .templatetags.metatags import include_metatags
from .utils import truncate_language_code_from_path, check_caching_enabled, get_cache_backend

UserModel = get_user_model()
HttpRequestDummy = namedtuple('HttpRequestDummy', ['path_info'])


class TestUtils(SimpleTestCase):

    def test_truncate_language_code_from_path(self):
        self.assertEqual(truncate_language_code_from_path('/'), '/')
        self.assertEqual(truncate_language_code_from_path('/en/'), '/')
        self.assertEqual(truncate_language_code_from_path('/end/'), '/end/')
        self.assertEqual(truncate_language_code_from_path('/en/services/'), '/services/')

    def test_check_caching_enabled_when_caching_disabled(self):
        self.assertFalse(check_caching_enabled())

    @override_settings(METATAGS_CACHE_ENABLED=True)
    def test_check_caching_enabled_when_caching_enabled(self):
        self.assertTrue(check_caching_enabled())


class TestTemplateTags(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.model_instance = UserModel.objects.create(username='test_user')
        cls.attached_to_model_instance_meta_tags = MetaTag.objects.create(
            title='test user title',
            keywords='test user keywords',
            description='test user description',
            content_object=cls.model_instance,
        )
        cls.attached_to_url_path_meta_tags = MetaTag.objects.create(
            url='/foo/bar/',
            title='test title',
            keywords='test keywords',
            description='test description',
        )

    def test_retrieve_attached_to_model_instance_meta_tags(self):
        meta_tags_template_context = include_metatags({}, self.model_instance)['meta_tags']
        self.assertEqual(self.attached_to_model_instance_meta_tags.title, meta_tags_template_context['title'])
        self.assertEqual(self.attached_to_model_instance_meta_tags.keywords, meta_tags_template_context['keywords'])
        self.assertEqual(
            self.attached_to_model_instance_meta_tags.description,
            meta_tags_template_context['description'],
        )

    def test_retrieve_attached_to_url_path_meta_tags(self):
        request = HttpRequestDummy('/foo/bar/')
        meta_tags_template_context = include_metatags({'request': request})['meta_tags']
        self.assertEqual(self.attached_to_url_path_meta_tags.title, meta_tags_template_context['title'])
        self.assertEqual(self.attached_to_url_path_meta_tags.keywords, meta_tags_template_context['keywords'])
        self.assertEqual(self.attached_to_url_path_meta_tags.description, meta_tags_template_context['description'])

    @override_settings(METATAGS_CACHE_ENABLED=True)
    def test_retrieve_attached_to_model_instance_cached_meta_tags(self):
        self.attached_to_model_instance_meta_tags._rebuild_cache()
        with self.assertNumQueries(0):
            meta_tags_template_context = include_metatags({}, self.model_instance)['meta_tags']
        self.assertEqual(self.attached_to_model_instance_meta_tags.title, meta_tags_template_context['title'])
        self.assertEqual(self.attached_to_model_instance_meta_tags.keywords, meta_tags_template_context['keywords'])
        self.assertEqual(
            self.attached_to_model_instance_meta_tags.description,
            meta_tags_template_context['description'],
        )
        self.attached_to_model_instance_meta_tags._invalidate_cache()

    @override_settings(METATAGS_CACHE_ENABLED=True)
    def test_retrieve_attached_to_url_path_cached_meta_tags(self):
        request = HttpRequestDummy('/foo/bar/')
        self.attached_to_url_path_meta_tags._rebuild_cache()
        with self.assertNumQueries(0):
            meta_tags_template_context = include_metatags({'request': request})['meta_tags']
        self.assertEqual(self.attached_to_url_path_meta_tags.title, meta_tags_template_context['title'])
        self.assertEqual(self.attached_to_url_path_meta_tags.keywords, meta_tags_template_context['keywords'])
        self.assertEqual(self.attached_to_url_path_meta_tags.description, meta_tags_template_context['description'])


class TestModels(TestCase):

    def setUp(self):
        self.model_instance = UserModel.objects.create(username='test_user')
        self.meta_tags = MetaTag.objects.create(
            title='test user title',
            keywords='test user keywords',
            description='test user description',
            content_object=self.model_instance,
        )

    def test_cascade_deletion_attached_to_model_instance_meta_tags(self):
        self.assertTrue(MetaTag.objects.exists())
        self.model_instance.delete()
        self.assertFalse(MetaTag.objects.exists())

    @override_settings(METATAGS_CACHE_ENABLED=True)
    def test_cascade_deletion_attached_to_model_instance_cached_meta_tags(self):
        self.meta_tags._rebuild_cache()
        cache = get_cache_backend()
        self.assertIsNotNone(cache.get(self.meta_tags._get_cache_key()))
        self.model_instance.delete()
        self.assertFalse(MetaTag.objects.exists())
        self.assertIsNone(cache.get(self.meta_tags._get_cache_key()))

    @override_settings(METATAGS_CACHE_ENABLED=True)
    def test_cached_meta_tags_deletion(self):
        self.meta_tags._rebuild_cache()
        cache = get_cache_backend()
        self.assertIsNotNone(cache.get(self.meta_tags._get_cache_key()))
        self.meta_tags.delete()
        self.assertIsNone(cache.get(self.meta_tags._get_cache_key()))
