from .models import Settings
from django.core.cache import cache


def get_settings(request):
    data = cache.get('settings')

    if data is None:
        # If the data doesn't exist in the cache, retrieve it from the data source
        data = Settings.objects.last()

        # Cache the data for future use
        cache.set('settings', data, timeout=60 * 60 * 24)

    context_data = {
        'settings_data': data,
    }
    return context_data
