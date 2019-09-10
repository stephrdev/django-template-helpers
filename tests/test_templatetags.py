import pytest
from django.template import Context, Template
from django.template.exceptions import TemplateSyntaxError


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

    def test_starspan(self):
        context = Context({'headline': 'Some ***headline*** text.'})
        result = Template(
            '{% load template_helpers %}{{ headline|starspan }}'
        ).render(context)
        assert result == 'Some <span>headline</span> text.'

    def test_split_custom_sep(self):
        context = Context()
        Template(
            '{% load template_helpers %}{% set test_var="foo-bar baz-lorem"|split:"-" %}'
        ).render(context)
        assert context['test_var'] == ['foo', 'bar baz', 'lorem']

    def test_merge_lists(self):
        context = Context({'first_list': ['a', 'b'], 'second_list': ['c', 'd']})
        result = Template(
            '{% load template_helpers %}'
            '{% for element in first_list|merge_lists:second_list %}'
            '{{ element }}'
            '{% endfor %}'
        ).render(context)
        assert result == 'abcd'

    def test_merge_lists_name_result(self):
        context = Context({'first_list': ['a', 'b'], 'second_list': ['c', 'd']})
        Template(
            '{% load template_helpers %}'
            '{% set new_list=first_list|merge_lists:second_list %}'
        ).render(context)
        assert context['new_list'] == ['a', 'b', 'c', 'd']

    def test_merge_lists_incorrect_call(self, settings):
        context = Context({'first_list': 'foo', 'second_list': 'bar'})

        with pytest.raises(TemplateSyntaxError):
            Template(
                '{% load template_helpers %}'
                '{{ first_list|merge_lists:second_list }}'
            ).render(context)

        with pytest.raises(TemplateSyntaxError):
            Template(
                '{% load template_helpers %}'
                '{{ first_list|merge_lists }}'
            ).render(context)

    def test_include_with(self):
        class MockObj:
            template_exposed_attributes = ['foo', 'bar', 'bazz']
            foo = 'test1'
            bar = 'test2'
            bazz = 'test3'
            eggs = 'test4'

        context = Context({'test_obj': MockObj()})
        result = Template(
            '{% load template_helpers %}'
            '{% include_with test_obj "test_include_with.html" bazz="new_bazz" %}'
        ).render(context)
        assert result.strip() == 'test1 test2 new_bazz'

    def test_include_with_no_object(self):
        context = Context({})
        with pytest.raises(TemplateSyntaxError):
            Template(
                '{% load template_helpers %}'
                '{% include_with test_obj "test_include_with.html" bazz="new_bazz" %}'
            ).render(context)

    def test_include_with_no_template_exposed_attributes(self):
        class MockObj:
            foo = 'test1'
            bar = 'test2'
            bazz = 'test3'
            eggs = 'test4'

        context = Context({'test_obj': MockObj()})
        with pytest.raises(TemplateSyntaxError):
            Template(
                '{% load template_helpers %}'
                '{% include_with test_obj "test_include_with.html" %}'
            ).render(context)

    def test_include_with_incorrect_args(self):
        context = Context({})
        with pytest.raises(TemplateSyntaxError):
            Template(
                '{% load template_helpers %}'
                '{% include_with test_obj "test_include_with.html" with var="a" %}'
            ).render(context)

        with pytest.raises(TemplateSyntaxError):
            Template(
                '{% load template_helpers %}'
                '{% include_with test_obj "test_include_with.html" with %}'
            ).render(context)

        with pytest.raises(TemplateSyntaxError):
            Template(
                '{% load template_helpers %}'
                '{% include_with test_obj "test_include_with.html" foo %}'
            ).render(context)

        with pytest.raises(TemplateSyntaxError):
            Template(
                '{% load template_helpers %}'
                '{% include_with test_obj "test_include_with.html" only %}'
            ).render(context)

        with pytest.raises(TemplateSyntaxError):
            Template(
                '{% load template_helpers %}'
                '{% include_with "test_include_with.html" %}'
            ).render(context)
