from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import MetaTag
from .utils import get_object_or_none, check_caching_enabled


@receiver(post_delete, dispatch_uid='delete_attached_meta_tags')
def delete_attached_meta_tags(sender, instance, **kwargs):
    meta_tags = get_object_or_none(
        klass=MetaTag,
        content_type__app_label=sender._meta.app_label,
        content_type__model=sender._meta.model_name,
        object_id=instance.pk,
    )
    if meta_tags is not None:
        meta_tags.delete()


@receiver(post_delete, sender=MetaTag, dispatch_uid='delete_meta_tags_from_cache')
def delete_meta_tags_from_cache(**kwargs):
    if check_caching_enabled():
        kwargs['instance']._invalidate_cache()
