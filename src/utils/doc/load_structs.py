import re
import json
import os

from utils.doc.load import get_str_from_doc


def get_structs(text: str):
    pattern = r"struct\s+\w+\s*\{[^{}]*\}"
    matches = re.findall(pattern, text)
    return matches


def get_struct_name(s: str):
    return s[len("struct "):s.find('{')]


def get_attributes(s: str):
    re_read_error = r"\s+\w+m_\w+"
    matches_read_error = re.findall(re_read_error, s)
    if matches_read_error:
        s = s.replace("m_", " m_")
        (s)
    re_attr = r"\w+\s+m_\w+(\[\d+\])?;"
    attributes = []

    matches = re.finditer(re_attr, s, re.MULTILINE)

    for matchNum, match in enumerate(matches, start=1):

        if match.group(0) is not None:
            attributes.append(match.group(0))

    return attributes


def get_attr_name(s: str):
    re_attr_name = r'm_\w+(\[\d+])?'
    name = re.search(re_attr_name, s)[0][2:]
    re_list_exception = r"^[^\[]+(?=\[\d+\])"
    list_exception_matches = re.search(re_list_exception, name)
    num = 0
    if list_exception_matches is not None:
        re_list_len = r"\[(\d+)\]"
        match = re.search(re_list_len, name)
        if match:
            num = int(match.group(1))
        name = list_exception_matches.group(0)
    name = format_attr_name(name)
    return name, num

def format_attr_name(name: str) -> str:
    parts = []
    
    for i, char in enumerate(name):
        if char.isupper():
            if i > 0 and (name[i - 1].islower() or (name[i - 1].isupper() and i > 0 and name[i - 1].islower())):
                parts.append('_')
            parts.append(char.lower())
        else:
            parts.append(char)
    
    formatted_name = ''.join(parts)
    
    return formatted_name


def get_attr_type(s: str):
    re_type = r'^\w+'
    type = re.search(re_type, s)[0]
    return type


def struct_to_json(struct: str):
    struct_name = get_struct_name(struct)
    attributes = get_attributes(struct)
    dic = {}
    for attribute in attributes:
        name = get_attr_name(attribute)
        type = get_attr_type(attribute)
        dic[name] = type
    return struct_name, dic


def type_is_array(type: str) -> int:
    match = re.search(r'\[(\d+)\]', type)
    if match:
        number = int(match.group(1))
        return number
    else:
        return 0


def structs_to_json_rec(text: str):
    struct_strs = get_structs(text)
    structs = {}
    for struct in struct_strs:
        struct_name = get_struct_name(struct)
        if "CarDamage" in struct_name:
            ()
        attributes = get_attributes(struct)
        attr = {}
        for attribute in attributes:
            name = get_attr_name(attribute)
            type = get_attr_type(attribute)
            iterator = type_is_array(name)
            if type in structs:
                type = structs[type]
            if iterator > 0:
                name = name[:name.find("[")]
                attr[name] = [type for i in range(iterator)]
                ()
            else:
                attr[name] = type
        structs[struct_name] = attr
    return structs


def write_to_json(struct: dict, name: str, path: str = os.path.join(".", "packets")):
    file_path = os.path.join(path, name) + ".json"
    os.makedirs(path, exist_ok=True)
    with open(file_path, "w+") as f:
        json.dump(struct, f, indent=4)


if __name__ == '__main__':
    path = "./Data Output from F1 23 v29x3.docx"
    text = get_str_from_doc(path)
    structs = structs_to_json_rec(text)
    for name, struct in structs.items():
        write_to_json(struct, name, os.path.join(".", "data", "F123"))
