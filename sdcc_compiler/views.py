import subprocess

from django.http import FileResponse, JsonResponse
from django.views.generic import TemplateView

import sdcc_compiler.parsing.asm_sections as asm_sections
import sdcc_compiler.parsing.cfile_sections as cfile_sections
from .forms import AddDirectoryForm, AddFileForm, AddSectionForm
from .models import Directory, File


class IndexView(TemplateView):
    template_name = 'sdcc_compiler/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        root_directories = Directory.objects.filter(parent__isnull=True)
        context['file_tree'] = [root.get_tree() for root in root_directories]
        root_files = File.objects.filter(directory__isnull=True)
        context['root_files'] = [{'name': f.name, 'id': f.id, 'is_accessible': f.is_accessible} for f in root_files]
        context['add_dir_form'] = AddDirectoryForm()
        context['add_file_form'] = AddFileForm()
        context['add_section_form'] = AddSectionForm()
        return context


def add_directory(request):
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
        return JsonResponse({'directory_id': new_directory.id})
    else:
        return JsonResponse({'error': 'Invalid form'})


def add_file(request):
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
        return JsonResponse({'file_id': new_file.id})
    else:
        return JsonResponse({'error': 'Invalid form'})


def view_file(request, file_id):
    file_to_view = File.objects.get(pk=file_id)
    with open(file_to_view.file.path, 'r') as f:
        file_content = f.read()

    sections = file_to_view.sections.all()
    section_dicts = [
        {'type': s.type, 'start': s.start_line, 'end': s.end_line}
        for s in sections
    ]
    data = {'file_content': file_content, 'sections': section_dicts}
    return JsonResponse(data)


def delete_directory(request, directory_id):
    directory_to_delete = Directory.objects.get(pk=directory_id)
    directory_to_delete.is_accessible = False
    directory_to_delete.save()
    return JsonResponse({'deleted_dir_id': directory_to_delete.id})


def delete_file(request, file_id):
    file_to_delete = File.objects.get(pk=file_id)
    file_to_delete.is_accessible = False
    file_to_delete.save()
    return JsonResponse({'deleted_file_id': file_to_delete.id})


def compile_file(request, file_id):
    standard = request.POST.get('standard_choice')
    optimizations = request.POST.getlist('optimization_choice', [])
    processor = request.POST.get('processor_choice')
    if processor == '-mmcs51':
        dependent = request.POST.get('mcs51_dependent_choice')
    elif processor == '-mz80':
        dependent = request.POST.get('z80_dependent_choice')
    else:
        dependent = request.POST.get('stm8_dependent_choice')
    file_to_compile = File.objects.get(pk=file_id)
    output_asm_path = 'media/compiled/output.asm'
    result = subprocess.run(['sdcc', '-o', output_asm_path, '-S', standard, *optimizations, processor, dependent,
                             file_to_compile.file.path], stderr=subprocess.PIPE)
    if result.returncode != 0:
        error_dicts = []
        error_lines = result.stderr.decode('utf-8').strip().split('\n')
        for line in error_lines:
            if ':' not in line or '/' not in line:
                continue
            split_line = line.split('/')
            error_message = split_line[-1]
            line_number = error_message.split(':')[1]
            error_dicts.append({'error_message': error_message, 'line_number': line_number})
        data = {'errors': error_dicts}
    else:
        asm_section_dicts = asm_sections.create_sections(output_asm_path)
        data = {'asm_sections': asm_section_dicts}
    return JsonResponse(data)


def download_asm(request):
    response = FileResponse(open('media/compiled/output.asm', 'rb'))
    response['Content-Disposition'] = 'attachment; filename="output.asm"'
    response['Content-Type'] = 'text/plain'
    return response


def add_section(request):
    form = AddSectionForm(request.POST)
    if form.is_valid():
        new_section = form.save(commit=False)
        file_id = form.cleaned_data['file']
        try:
            file = File.objects.get(id=file_id)
        except File.DoesNotExist:
            file = None
        new_section.file = file
        new_section.save()
        return JsonResponse({'type': new_section.type, 'start': new_section.start_line, 'end': new_section.end_line})
    else:
        return JsonResponse({'error': 'Invalid form'})
