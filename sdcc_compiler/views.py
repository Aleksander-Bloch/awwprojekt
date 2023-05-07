import subprocess

from django.http import FileResponse
from django.shortcuts import redirect
from django.views.generic import TemplateView

import sdcc_compiler.parsing.asm_sections as asm_sections
import sdcc_compiler.parsing.cfile_sections as cfile_sections
from .forms import AddDirectoryForm, AddFileForm
from .models import Directory, File


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
        context['editor_file_id'] = self.request.session.get('editor_file_id', None)
        context['asm_sections'] = self.request.session.get('asm_sections', [])
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
    request.session['editor_file_id'] = file_id
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


def compile_file(request):
    if not request.session.get('editor_file_id', None):
        return redirect('index')
    standard = request.POST.get('standard_choice')
    optimizations = request.POST.getlist('optimization_choice', [])
    processor = request.POST.get('processor_choice')
    if processor == '-mmcs51':
        dependent = request.POST.get('mcs51_dependent_choice')
    elif processor == '-mz80':
        dependent = request.POST.get('z80_dependent_choice')
    else:
        dependent = request.POST.get('stm8_dependent_choice')
    file_to_compile = File.objects.get(pk=request.session['editor_file_id'])
    output_asm_path = 'media/compiled/output.asm'
    subprocess.run(['sdcc', '-o', output_asm_path, '-S', standard, *optimizations, processor, dependent,
                    file_to_compile.file.path])
    asm_section_dicts = asm_sections.create_sections(output_asm_path)
    request.session['asm_sections'] = asm_section_dicts

    return redirect('index')


def download_asm(request):
    if not request.session.get('asm_sections', None):
        return redirect('index')
    response = FileResponse(open('media/compiled/output.asm', 'rb'))
    response['Content-Disposition'] = 'attachment; filename="output.asm"'
    response['Content-Type'] = 'text/plain'
    return response


# Server-side implementation of manual sectioning of the c file.
def create_new_section(request):
    if not request.session.get('editor_file_id', None):
        return redirect('index')
    file_to_compile = File.objects.get(pk=request.session['editor_file_id'])
    start_line = request.POST.get('start_line')
    end_line = request.POST.get('end_line')
    section_type = request.POST.get('section_type')
    section = file_to_compile.sections.create(start_line=start_line, end_line=end_line, type=section_type)
    section.save()
    return redirect('index')


def merge_two_sections_into_one(request):
    if not request.session.get('editor_file_id', None):
        return redirect('index')
    file_to_compile = File.objects.get(pk=request.session['editor_file_id'])
    first_section_id = request.POST.get('first_section_id')
    second_section_id = request.POST.get('second_section_id')
    first_section = file_to_compile.sections.get(pk=first_section_id)
    second_section = file_to_compile.sections.get(pk=second_section_id)
    first_section.end_line = second_section.end_line
    first_section.content += second_section.content
    first_section.save()
    second_section.delete()
    return redirect('index')
