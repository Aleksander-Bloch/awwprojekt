import re
from re import Pattern

from sdcc_compiler.models import Section, SectionType
from sdcc_compiler.models import File


def create_sections_by_type(regex: Pattern[str], cfile_text: str, file: File, section_type: SectionType):
    sections = []
    for match in regex.finditer(cfile_text):
        section = Section(start_line=cfile_text.count('\n', 0, match.start()) + 1,
                          end_line=cfile_text.count('\n', 0, match.end()) + 1,
                          content=match.group(),
                          type=section_type,
                          file=file)
        sections.append(section)
    return sections


def add_parent_fk(section_db_objects):
    section_db_objects.sort(key=lambda x: x.start_line)
    for i in range(len(section_db_objects)):
        section = section_db_objects[i]
        start_line = section.start_line
        end_line = section.end_line
        for j in range(i + 1, len(section_db_objects)):
            if section_db_objects[j].start_line > end_line:
                break
            if section_db_objects[j].start_line >= start_line and section_db_objects[j].end_line <= end_line:
                section_db_objects[j].parent = section
                section_db_objects[j].save()


def create_sections(file: File):
    proc_re = re.compile(r'(int|void|char|float|double|bool|\w+\s*\*)\s+\w+\(.*?\)\s*\{.*?}', re.DOTALL)
    comment_re = re.compile(r'(/\*.*?\*/|//.*?$)', re.DOTALL | re.MULTILINE)
    directive_re = re.compile(r'#\s*\w+.*?\n')
    var_decl_re = re.compile(r'(int|char|float|double|bool)\s+\**\s*\w+\s*(=\s*[^;]+)?\s*;')
    inline_asm_re = re.compile(r'(asm|__asm__)\s*\(.*?\)\s*;', re.DOTALL)

    file_path = file.file.path
    with open(file_path, 'r') as f:
        cfile_text = f.read()

    sections = []
    sections += create_sections_by_type(proc_re, cfile_text, file, SectionType.PROCEDURE)
    sections += create_sections_by_type(comment_re, cfile_text, file, SectionType.COMMENT)
    sections += create_sections_by_type(directive_re, cfile_text, file, SectionType.COMPILER_DIRECTIVE)
    sections += create_sections_by_type(var_decl_re, cfile_text, file, SectionType.VARIABLE_DECLARATION)
    sections += create_sections_by_type(inline_asm_re, cfile_text, file, SectionType.INLINE_ASSEMBLY)

    section_db_objects = Section.objects.bulk_create(sections)
    add_parent_fk(section_db_objects)
