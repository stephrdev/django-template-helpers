from template_helpers.views import GenericTemplateView


class TestGenericTemplateView:

    def test_get_template_names(self, client):
        view = GenericTemplateView(kwargs={'template': 'foo'})
        assert view.get_template_names() == ['tests/foo.html']

    def test_get_template_names_without_template(self, client):
        view = GenericTemplateView(kwargs={'template': None})
        assert view.get_template_names() == ['tests/index.html']
