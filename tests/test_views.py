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

    def test_get_template_base_dir(self, rf):
        view = GenericTemplateView.as_view(template_base_dir='test_dir')
        request = rf.get('/')

        response = view(request)
        assert response.template_name[0] == 'test_dir/index.html'

        response = view(request, **{'template': 'test123'})
        assert response.template_name[0] == 'test_dir/test123.html'

        view = GenericTemplateView.as_view(template_base_dir='test_dir/foo/bar')

        response = view(request)
        assert response.template_name[0] == 'test_dir/foo/bar/index.html'

        response = view(request, **{'template': 'abc654/test123'})
        assert response.template_name[0] == 'test_dir/foo/bar/abc654/test123.html'
