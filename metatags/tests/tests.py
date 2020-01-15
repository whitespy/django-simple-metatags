from collections import namedtuple

from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import MetaTag
from ..templatetags.meta_tags import include_meta_tags
from ..utils import truncate_language_code_from_path

UserModel = get_user_model()
HttpRequestDummy = namedtuple('HttpRequestDummy', ['path_info'])


class TestMetaTags(TestCase):

    def test_truncate_language_code_from_path(self):
        self.assertEqual(truncate_language_code_from_path('/'), '/')
        self.assertEqual(truncate_language_code_from_path('/en/'), '/')
        self.assertEqual(truncate_language_code_from_path('/end/'), '/end/')
        self.assertEqual(truncate_language_code_from_path('/en/services/'), '/services/')

    def test_get_meta_tags_for_object(self):
        test_user = UserModel.objects.create(username='test_user')
        meta_tag_model_instance = MetaTag.objects.create(
            title='test user title',
            keywords='test user keywords',
            description='test user description',
            content_object=test_user,
        )
        meta_tag_template_context_dict = include_meta_tags({}, test_user)
        self.assertEqual(meta_tag_model_instance.title, meta_tag_template_context_dict['meta_tags'].title)
        self.assertEqual(meta_tag_model_instance.keywords, meta_tag_template_context_dict['meta_tags'].keywords)
        self.assertEqual(meta_tag_model_instance.description, meta_tag_template_context_dict['meta_tags'].description)

    def test_get_meta_tags_by_url_path(self):
        request = HttpRequestDummy('/foo/bar/')
        meta_tag_model_instance = MetaTag.objects.create(
            url=request.path_info,
            title='test title',
            keywords='test keywords',
            description='test description',
        )
        meta_tag_template_context_dict = include_meta_tags({'request': request})
        self.assertEqual(meta_tag_model_instance.title, meta_tag_template_context_dict['meta_tags'].title)
        self.assertEqual(meta_tag_model_instance.keywords, meta_tag_template_context_dict['meta_tags'].keywords)
        self.assertEqual(meta_tag_model_instance.description, meta_tag_template_context_dict['meta_tags'].description)

    def test_delete_attached_meta_tags(self):
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
