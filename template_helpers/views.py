import os

from django.views.generic import TemplateView


class GenericTemplateView(TemplateView):
    base_template_dir = ''

    def get_base_directory(self, **kwargs):
        return self.kwargs.get('base_template_dir') or self.base_template_dir

    def get_template_names(self):
        template_filename = '%s.html' % (self.kwargs.get('template') or 'index')
        base_dir = self.get_base_directory()
        return [os.path.join(base_dir, template_filename)]
