from django import template as django_template
from django.template.base import TemplateSyntaxError, token_kwargs
from django.template.defaultfilters import stringfilter
from django.template.loader_tags import IncludeNode, construct_relative_path


register = django_template.Library()


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


@register.simple_tag(name='merge_lists', takes_context=True)
def merge_lists(context, as_var, source_list, list_to_merge):
    """
    The ``merge_lists`` template tag combines two lists under a given name.

    .. code-block:: text

        {% merge_lists 'new_list' source_list list_to_merge %}
        {{ new_list }}

    """
    if not source_list and not type(source_list) == list and not type(list_to_merge) == list:
        context[as_var] = None
        return ''

    context[as_var] = source_list + list_to_merge

    return ''


class IncludeWithNode(IncludeNode):

    def __init__(
            self, with_object, template, *args, extra_context=None,
            isolated_context=False, **kwargs):
        self.with_object = django_template.Variable(with_object)
        super().__init__(
            template, *args, extra_context=extra_context,
            isolated_context=isolated_context, **kwargs)

    def render(self, context):
        obj = None
        try:
            obj = self.with_object.resolve(context)
        except django_template.VariableDoesNotExist:
            pass

        exposed_vars = getattr(obj, 'exposed', [])
        for var in exposed_vars:
            context[var] = getattr(obj, var)

        return super().render(context)


def _parse_with_options(bits, start_position, parser):
    """
    Helper for parsig with templatetag arguments.

    Based on:
    https://github.com/django/django/blob/master/django/template/loader_tags.py
    #L295-L312

    """
    options = {}
    remaining_bits = bits[start_position:]

    while remaining_bits:
        option = remaining_bits.pop(0)
        if option in options:
            raise TemplateSyntaxError(
                'The %r option was specified more than once.' % option)
        if option == 'with':
            value = token_kwargs(remaining_bits, parser, support_legacy=False)
            if not value:
                raise TemplateSyntaxError(
                    '"with" in %r tag needs at least one keyword argument.' % bits[0])
        elif option == 'only':
            value = True
        else:
            raise TemplateSyntaxError(
                'Unknown argument for %r tag: %r.' % (bits[0], option))
        options[option] = value

    return options


@register.tag('include_with')
def do_include_with(parser, token):
    """
    The ``include_with`` extends include template tag to avoid long with statements.
    It takes object as first argument and adds its exposed attributes
    into context available in included template. It requires that object has
    list of exposed attributes.

    .. code-block:: text

        {% include_with obj 'path/to/included/template.html' %}

    It is also possible to use with syntax to overwrite some of exposed
    attributes or add new ones.

    .. code-block:: text

        {% include_with obj 'path/to/included/template.html' with foo='bar'%}

    """
    bits = token.split_contents()

    if len(bits) < 3:
        raise TemplateSyntaxError(
            "%r tag takes at least two argument: the object with exposed "
            "attributes and the name of the template to "
            "be included." % bits[0]
        )

    options = _parse_with_options(bits, 3, parser)

    isolated_context = options.get('only', False)
    namemap = options.get('with', {})
    bits[1] = construct_relative_path(parser.origin.template_name, bits[1])
    return IncludeWithNode(
        bits[1], parser.compile_filter(bits[2]), extra_context=namemap,
        isolated_context=isolated_context)
