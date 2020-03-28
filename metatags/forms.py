from django import forms
from django.conf import settings
from django.utils.translation import gettext, gettext_lazy as _

from .models import MetaTag


class MetaTagForm(forms.ModelForm):
    url = forms.RegexField(
        label=_('URL-path'),
        max_length=100,
        regex=r'^[-\w/\.~]+$',
        help_text=_("Example: '/about/contact/'. Make sure to have leading and trailing slashes."),
        error_messages={
            'invalid': _(
                "This value must contain only letters, numbers, dots, underscores, dashes, slashes or tildes."
            ),
        },
    )

    class Meta:
        fields = ('url', 'title', 'keywords', 'description')

    def clean_url(self):
        url = self.cleaned_data['url']

        if not url.startswith('/'):
            raise forms.ValidationError(gettext('URL is missing a leading slash.'), code='missing_leading_slash')

        if (not url.endswith('/') and settings.APPEND_SLASH and
                'django.middleware.common.CommonMiddleware' in settings.MIDDLEWARE):
            raise forms.ValidationError(gettext('URL is missing a trailing slash.'), code='missing_trailing_slash')

        if MetaTag.objects.filter(url=url).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError(
                gettext('Meta tags for a given URL-path have already been identified.'),
                code='duplicate_url',
            )

        return url
