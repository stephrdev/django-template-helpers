from django import template
from django.template.defaultfilters import stringfilter


register = template.Library()


@register.simple_tag(name='set', takes_context=True)
def set_tag(context, **kwargs):
    """
    The `set`` template tag add one or more context variables to the current
    template context. The context stack is respected.

    .. code-block:: text

        {% set foo="bar" baz=1 %}
        {{ foo }}
        {{ baz }}

    """
    # We cannot use context.update - this would break the context push/pop mech.
    for key, value in kwargs.items():
        context[key] = value
    return ''


@register.filter
@stringfilter
def split(value, sep=' '):
    """
    The ``split`` template filter splits a given string by spaces. If you want
    to split by something else, provide the devider as a argument to the filter.

    .. code-block:: text

        {{ "foo bar"|split }}
        {{ "foo-bar"|split"-" }}

    """
    return value.split(sep)
