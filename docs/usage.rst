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


Add extra span element inside text
----------------------------------

To add extra <span> element inside a string use ``starspan`` filter.

.. code-block:: text

    class SomeModel(models.Model):
      headline = models.CharField(help_text=_('Use ***my text*** to highlight "my text".'))
      ...

.. code-block:: text

    {% load template_helpers %}

    {{ headline|starspan }}


Append a list to another list in template
-----------------------------------------

If you need to join lists within your templates, use the ``merge_list`` filter.

.. code-block:: text

    {% load template_helpers %}

    {% for element in first_list|merge_list:second_list %}
      {{ element }}
    {% endfor %}

To make the result list persistent use ``merge_list`` filter in combination with ``set`` template tag.

.. code-block:: text

    {% load template_helpers %}

    {% set new_list=first_list|merge_list:second_list %}


Add object attributes to context of included template
-----------------------------------------------------

If you have an object with many attributes which need to be directly accessible
in included template, use the ``include_with`` tag.

Suppose you have a Person model:

.. code-block:: text

  class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

Define exposed attributes on it:

.. code-block:: text

  class Person(models.Model):
    template_exposed_attributes = ['first_name', 'last_name']
    ...

Then you can use ``include_with`` template tag:

.. code-block:: text

    {% load template_helpers %}

    {% include_with person 'some/template.html' %}

Instead of

.. code-block:: text

    {% include 'some/template.html' with first_name=person.first_name last_name=person.last_name %}

It is also possible to overwrite / add additional kwargs.

.. code-block:: text

    {% load template_helpers %}

    {% include_with person 'some/template.html' first_name='Laurel' best_friend='Hardy' %}


Using GenericTemplateView
-------------------------

``GenericTemplateView`` is a ``TemplateView`` extension, that allows including
static pages. The template path is encoded in url as ``template`` keyword argument,
and the templates base directory can be set with ``template_base_dir``
keyword argument in ``GenericTemplateView.as_view`` call.


The ``GenericTemplateView`` can be used e.g. for template testing.

.. code-block:: text

    if settings.DEBUG:
        urlpatterns += [
            url(
                r'^tests/((?P<template>[\w\-\/]+)/)?$',
                GenericTemplateView.as_view(template_base_dir='mytests')
            ),

If test templates are located in templates/mytests/...
(e.g. templates/mytests/base/buttons/buttons.html) we can now hit them by calling
e.g. localhost:8000/tests/base/buttons/buttons url.

If no ``template_base_dir`` or ``template`` are specified, the view will try to render index.html.
For more elaborate behavior overwrite the ``get_template_base_dir`` and ``get_template_names``
methods.
