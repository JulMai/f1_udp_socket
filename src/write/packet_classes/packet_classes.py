import os

from utils.doc.load_structs import get_structs, get_str_from_doc, get_struct_name, get_attributes, get_attr_name, get_attr_type


_ctypes_types = [
    'int8',
    'int16',
    'uint8',
    'uint16',
    'uint32',
    'uint64',
    'float',
    'char',
    'double'
]


def get_type_class(type: str):
    if type in _ctypes_types:
        return f"ctypes.c_{type}"
    else:
        return type


def get_class_str_from_struct_text(text: str) -> str:
    name = get_struct_name(text)
    class_str = f"class {name}(Packet):\n"
    tab = "\t"
    class_str += f"{tab}_fields_ = [\n"
    tab += "\t"

    attributes = get_attributes(text)
    for attribute in attributes:
        attr_name = get_attr_name(attribute)
        attr_type = get_attr_type(attribute)
        attr_class = get_type_class(attr_type)
        class_str += f"{tab}(\"{attr_name}\", {attr_class}),\n"
    tab = tab[:-1]
    class_str += f"{tab}]\n"
    return class_str


if __name__ == '__main__':
    path = "./Data Output from F1 23 v29x3.docx"
    path_template = os.path.join(os.path.dirname(__file__), "packets.py.templ")
    path_out = "./packets.py"
    with open(path_out, 'w') as f:
        with open(path_template, 'r') as f_templ:
            templ_text = f_templ.read()
        f.write(templ_text + "\n\n")

    text = get_str_from_doc(path)
    structs = get_structs(text)

    for struct in structs:
        class_str = get_class_str_from_struct_text(struct)
        with open(path_out, 'a') as f:
            f.write(class_str + "\n\n")
