from django.core.management.base import BaseCommand


from ...utils import check_caching_enabled, reset_meta_tags_cache


class Command(BaseCommand):
    help = 'Resets meta tags cache.'

    def handle(self, **options):
        if check_caching_enabled():
            reset_meta_tags_cache()
            self.stdout.write(self.style.SUCCESS('Meta tags has been successfully reset.'))
        else:
            self.stderr.write('Meta tags caching was not enabled.')
