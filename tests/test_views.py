from template_helpers.views import GenericTemplateView


class TestGenericTemplateView:

    def test_get_template_names(self):
        view = GenericTemplateView()
        view.kwargs = {}

        view.kwargs['template'] = None
        assert view.get_template_names() == ['index.html']

        view.kwargs['template'] = 'test123'
        assert view.get_template_names() == ['test123.html']

        view.kwargs['template'] = 'abc654/test123'
        assert view.get_template_names() == ['abc654/test123.html']

        view.kwargs['base_template_dir'] = 'foo'
        view.kwargs['template'] = None
        assert view.get_template_names() == ['foo/index.html']

        view.kwargs['base_template_dir'] = 'foo'
        view.kwargs['template'] = 'test123'
        assert view.get_template_names() == ['foo/test123.html']

        view.kwargs['base_template_dir'] = 'foo/bar/bazz'
        view.kwargs['template'] = 'abc654/test123'
        assert view.get_template_names() == ['foo/bar/bazz/abc654/test123.html']
