from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from .forms import AddDirectoryForm, AddFileForm
from .models import Directory, File


class IndexView(TemplateView):
    template_name = 'sdcc_compiler/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        root_directories = Directory.objects.filter(parent__isnull=True)
        context['file_tree'] = [root.get_tree() for root in root_directories]
        root_files = File.objects.filter(directory__isnull=True)
        context['root_files'] = [{'name': f.name, 'id': f.id} for f in root_files]
        add_dir_form = AddDirectoryForm()
        context['add_dir_form'] = add_dir_form
        add_file_form = AddFileForm()
        context['add_file_form'] = add_file_form
        return context


def add_directory(request):
    if request.method == 'POST':
        form = AddDirectoryForm(request.POST)
        if form.is_valid():
            parent_id = form.cleaned_data['parent']
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            try:
                parent = Directory.objects.get(id=parent_id)
            except Directory.DoesNotExist:
                parent = None
            new_directory = Directory(parent=parent, name=name, description=description)
            new_directory.save()
            return redirect('index')
    form = AddDirectoryForm()
    return render(request, 'sdcc_compiler/index.html', {'add_dir_form': form})


def add_file(request):
    if request.method == 'POST':
        form = AddFileForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            uploaded_file = form.cleaned_data['file']
            directory_id = form.cleaned_data['directory']
            try:
                directory = Directory.objects.get(id=directory_id)
            except Directory.DoesNotExist:
                directory = None
            new_file = File(directory=directory, name=name, file=uploaded_file)
            new_file.save()
            return redirect('index')
    form = AddFileForm()
    return render(request, 'sdcc_compiler/index.html', {'add_file_form': form})


def view_file(request, file_id):
    file_to_view = File.objects.get(pk=file_id)
    with open(file_to_view.file.path, 'r') as f:
        file_content = f.read()

    context = {'file_content': file_content}
    return render(request, 'sdcc_compiler/index.html', context)
