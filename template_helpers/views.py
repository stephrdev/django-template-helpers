import os

from django.views.generic import TemplateView


class GenericTemplateView(TemplateView):
    template_base_dir = ''

    def get_template_base_dir(self):
        return self.template_base_dir

    def get_template_names(self):
        template_filename = '%s.html' % (self.kwargs.get('template') or 'index')
        base_dir = self.get_template_base_dir()
        return [os.path.join(base_dir, template_filename)]
