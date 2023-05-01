from django.views.generic import ListView, TemplateView

from sdcc_compiler.models import Directory


class IndexView(TemplateView):
    template_name = 'sdcc_compiler/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        root_directories = Directory.objects.filter(parent__isnull=True)
        context['file_tree'] = [root.get_tree() for root in root_directories]
        return context
