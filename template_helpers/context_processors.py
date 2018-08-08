from django.conf import settings as django_settings


def settings(request):
    """
    The ``settings`` context processor adds all settings from the
    ``TEMPLATE_EXPOSED_SETTINGS`` configuration to the template context.
    """
    parameters = getattr(django_settings, 'TEMPLATE_EXPOSED_SETTINGS', ['DEBUG'])

    context = {}
    for parameter in parameters:
        context[parameter] = getattr(django_settings, parameter, None)

    return context
