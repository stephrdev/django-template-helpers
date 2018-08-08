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
