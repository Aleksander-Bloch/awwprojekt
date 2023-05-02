from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from .forms import DirectoryForm
from .models import Directory


class IndexView(TemplateView):
    template_name = 'sdcc_compiler/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        root_directories = Directory.objects.filter(parent__isnull=True)
        context['file_tree'] = [root.get_tree() for root in root_directories]
        add_dir_form = DirectoryForm()
        context['add_dir_form'] = add_dir_form
        return context


def add_directory(request):
    if request.method == 'POST':
        form = DirectoryForm(request.POST)
        if form.is_valid():
            parent_id = form.cleaned_data['parent']
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            parent = Directory.objects.get(id=parent_id)
            new_directory = Directory(parent=parent, name=name, description=description)
            new_directory.save()
            return redirect('index')
    form = DirectoryForm()
    return render(request, 'sdcc_compiler/index.html', {'add_dir_form': form})
