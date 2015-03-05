from django.conf import settings

__all__ = []

_DEFAULTS = {
    'BOOTSTRAP_TOOLTIPS': True
}

for key, value in _DEFAULTS.iteritems():
    try:
        getattr(settings, key)
    except AttributeError:
        setattr(settings, key, value)
    # Suppress errors from DJANGO_SETTINGS_MODULE not being set
    except ImportError:
        pass
