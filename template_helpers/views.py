import os

from django.views.generic import TemplateView


class GenericTemplateView(TemplateView):

    def get_base_directory(self, **kwargs):
        return self.kwargs.get('base_dir') or ''

    def get_template_names(self):
        template_filename = '%s.html' % (self.kwargs.get('template') or 'index')
        base_dir = self.get_base_directory()
        return [os.path.join(base_dir, template_filename)]
