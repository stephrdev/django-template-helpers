from django.template import Context, Template


class TestTemplateTags:

    def test_set_tag(self):
        context = Context()
        Template(
            '{% load template_helpers %}{% set test_var="Some data" %}'
        ).render(context)
        assert context['test_var'] == 'Some data'

    def test_split_default_sep(self):
        context = Context()
        Template(
            '{% load template_helpers %}{% set test_var="foo bar baz"|split %}'
        ).render(context)
        assert context['test_var'] == ['foo', 'bar', 'baz']

    def test_split_custom_sep(self):
        context = Context()
        Template(
            '{% load template_helpers %}{% set test_var="foo-bar baz-lorem"|split:"-" %}'
        ).render(context)
        assert context['test_var'] == ['foo', 'bar baz', 'lorem']

    def test_merge_lists(self):
        context = Context({'first_list': ['a', 'b'], 'second_list': ['c', 'd']})
        Template(
            '{% load template_helpers %}{% merge_lists "test_list" first_list second_list %}'
        ).render(context)
        assert context['test_list'] == ['a', 'b', 'c', 'd']
