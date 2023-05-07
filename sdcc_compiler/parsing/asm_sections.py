def make_section_dict(in_header, current_section_lines):
    return {"is_header": in_header, "content": "".join(current_section_lines)}


def create_sections(asm_file):
    with open(asm_file, 'r') as f:
        lines = f.readlines()

    section_dicts = []
    current_section_lines = []
    in_header = False

    for line in lines:
        if in_header:
            if line.startswith(";-"):
                current_section_lines.append(line)
                section_dicts.append(make_section_dict(in_header, current_section_lines))
                current_section_lines = []
                in_header = False
            elif not line.startswith(";"):
                section_dicts.append(make_section_dict(in_header, current_section_lines))
                current_section_lines = [line]
                in_header = False
            else:
                current_section_lines.append(line)
        else:
            if line.startswith(";-"):
                if current_section_lines:
                    section_dicts.append(make_section_dict(in_header, current_section_lines))
                current_section_lines = [line]
                in_header = True
            else:
                current_section_lines.append(line)

    if current_section_lines:
        section_dicts.append(make_section_dict(in_header, current_section_lines))

    return section_dicts
