from django.shortcuts import redirect
from django.views.generic import TemplateView

from .forms import AddDirectoryForm, AddFileForm
from .models import Directory, File
import sdcc_compiler.parsing.cfile_sections as cfile_sections


class IndexView(TemplateView):
    template_name = 'sdcc_compiler/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        root_directories = Directory.objects.filter(parent__isnull=True)
        context['file_tree'] = [root.get_tree() for root in root_directories]
        root_files = File.objects.filter(directory__isnull=True)
        context['root_files'] = [{'name': f.name, 'id': f.id, 'is_accessible': f.is_accessible} for f in root_files]
        add_dir_form = AddDirectoryForm()
        context['add_dir_form'] = add_dir_form
        add_file_form = AddFileForm()
        context['add_file_form'] = add_file_form
        context['file_content'] = self.request.session.get('file_content', '')
        context['sections'] = self.request.session.get('sections', [])
        return context


def add_directory(request):
    if request.method == 'POST':
        form = AddDirectoryForm(request.POST)
        if form.is_valid():
            new_directory = form.save(commit=False)
            parent_id = form.cleaned_data['parent']
            try:
                parent = Directory.objects.get(id=parent_id)
            except Directory.DoesNotExist:
                parent = None
            new_directory.parent = parent
            new_directory.save()
    return redirect('index')


def add_file(request):
    if request.method == 'POST':
        form = AddFileForm(request.POST, request.FILES)
        if form.is_valid():
            new_file = form.save(commit=False)
            directory_id = form.cleaned_data['directory']
            try:
                directory = Directory.objects.get(id=directory_id)
            except Directory.DoesNotExist:
                directory = None
            new_file.directory = directory
            new_file.save()
            cfile_sections.create_sections(new_file)
    return redirect('index')


def view_file(request, file_id):
    file_to_view = File.objects.get(pk=file_id)
    with open(file_to_view.file.path, 'r') as f:
        file_content = f.read()

    request.session['file_content'] = file_content
    sections = file_to_view.sections.all()
    section_dicts = [
        {'type': s.type, 'start': s.start_line, 'end': s.end_line, 'status': s.status}
        for s in sections
    ]
    request.session['sections'] = section_dicts
    return redirect('index')


def delete_directory(request, directory_id):
    directory_to_delete = Directory.objects.get(pk=directory_id)
    directory_to_delete.is_accessible = False
    directory_to_delete.save()
    return redirect('index')


def delete_file(request, file_id):
    file_to_delete = File.objects.get(pk=file_id)
    file_to_delete.is_accessible = False
    file_to_delete.save()
    return redirect('index')
