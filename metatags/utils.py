from django.utils.translation import get_language_from_path


def truncate_language_code(path):
    """
    Truncates language code from URL-path.
    """
    language_code = get_language_from_path(path)
    if language_code:
        return path.replace('/{}'.format(language_code), '', 1) or '/'
    return path
