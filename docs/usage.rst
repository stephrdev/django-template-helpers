Usage
=====

Expose settings to template context
-----------------------------------

In order to expose settings to the template context, you have to add the
``template_helpers.context_processors.settings`` context processor to your
``TEMPLATES`` configuration block.

When done, add a list of settings to expose to your configuration.

.. code-block:: python

    TEMPLATE_EXPOSED_SETTINGS = (
        'DEBUG',
        'SOME_PUBLIC_API_TOKEN',
    )


Settings new template context variables
---------------------------------------

If you need to add new context variables within your templates, use the ``set`` tag.


.. code-block:: text

    {% load template_helpers %}

    {% set foo="Ipsum" }}

    Lorem {{ foo }}

The output will be

.. code-block:: text

    Lorem Ipsum


Splitting a string
------------------

To split a string for iteration, you can use the ``split`` filter.
The filter allows to pass an alternative delimiter, default is " ".

.. code-block:: text

    {% load template_helpers %}

    {% for item in "item1,item2"|split:"," %}
        Item: {{ item }}
    {% endfor %}

The output will be

.. code-block:: text

    Item: item1
    Item: item2


Using GenericTemplateView
-------------------------

GenericTemplateView is an extension of TemplateView that allows including
static pages via encoding template name and base directory in the url.
It can be used e.g. for testing your templates.

.. code-block:: text

    if settings.DEBUG:
        urlpatterns += [
            url(
                r'^(?P<base_dir>[\w\-]+)/((?P<template>[\w\-\/]+)/)?$',
                GenericTemplateView.as_view()
            ),

If test templates are located in templates/tests/...
(e.g. templates/tests/base/buttons/buttons.html) we can now hit them by calling
e.g. localhost:8000/tests/base/buttons/buttons url.

If no base_dir or template names are given, the view will try to render index.html.
For more elaborate behavior the ``get_template_names`` method can be overwritten.
