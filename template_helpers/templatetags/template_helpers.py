import re

from django import VERSION as django_version
from django import template
from django.template.base import TemplateSyntaxError
from django.template.defaultfilters import stringfilter
from django.template.library import parse_bits
from django.template.loader_tags import IncludeNode, construct_relative_path
from django.utils.html import conditional_escape, mark_safe


STARSPAN_RE = re.compile(r'(\*\*\*)(.+?)\1')

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


@register.filter
@stringfilter
def starspan(value):
    """
    The ``starspan`` template filter adds extra span element to star
    indicated text ("***text***").

    .. code-block:: text

        {{ some_text_variable|starspan }}

    """
    return mark_safe(STARSPAN_RE.sub(r'<span>\2</span>', conditional_escape(value)))


@register.filter
def merge_list(value, list_to_merge):
    """
    The ``merge_list`` filter combines two lists.

    .. code-block:: text

        {% for element in first_list|merge_list:second_list %}
            {{ element }}
        {% endfor %}

    To make the result list persistent use in combination with set tag.

    .. code-block:: text

        {% set new_list=first_list|merge_lists:second_list %}

    """
    if not type(value) == list or not type(list_to_merge) == list:
        raise TemplateSyntaxError(
           'Value and argument for merge_lists filter should be both of type '
           'list. Got "{0}" and "{1}".'.format(value, list_to_merge))

    return value + list_to_merge


class IncludeWithNode(IncludeNode):

    def __init__(
            self, with_object, template_name, *args, extra_context=None,
            **kwargs):
        self.with_object = template.Variable(with_object)
        super().__init__(
            template_name, *args, extra_context=extra_context,
            isolated_context=False, **kwargs)

    def render(self, context):
        obj = None
        try:
            obj = self.with_object.resolve(context)
        except template.VariableDoesNotExist as exc:
            raise TemplateSyntaxError(
                'Object {0} needs to be available in template context.'.format(
                    self.with_object.var)) from exc
        if not obj:
            raise TemplateSyntaxError(
               'Object {0} is None. Provide corrct value.'.format(
                    self.with_object.var))

        exposed_attrs = getattr(obj, 'template_exposed_attributes', None)
        if exposed_attrs is None or type(exposed_attrs) != list:
            raise TemplateSyntaxError(
                'Object {0} should have template_exposed_attributes set'.format(
                    self.with_object.var))

        for exposed_attr in exposed_attrs:
            context[exposed_attr] = getattr(obj, exposed_attr)
        return super().render(context)


@register.tag('include_with')
def do_include_with(parser, token):
    """
    Include template with object attributes injected to context.
    It takes object and template path as arguments.
    Object should have template_exposed_attributes list defined.

    .. code-block:: text

        {% include_with obj 'path/to/included/template.html' %}

    It is also possible to overvrite / add additional kwaegs.

    .. code-block:: text

        {% include_with obj 'path/to/included/template.html' foo='bar'%}

    """
    bits = token.split_contents()

    if django_version[0] >= 2:
        options = parse_bits(
            parser, bits[1:], ['with_object', 'template_name'], False, True,
            None, [], None, False, 'include_with')
    else:
        options = parse_bits(
            parser, bits[1:], ['with_object', 'template_name'], False, True,
            None, False, 'include_with')

    bits[2] = construct_relative_path(parser.origin.template_name, bits[2])
    template_filter = parser.compile_filter(bits[2])

    return IncludeWithNode(
        bits[1], template_filter, extra_context=options[1])
