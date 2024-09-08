import os

from utils.doc.load_structs import get_structs, get_str_from_doc, get_struct_name, get_attributes, get_attr_name, get_attr_type
from utils.doc.appendices import packet_ids

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
        attr_name, attr_num = get_attr_name(attribute)
        attr_type = get_attr_type(attribute)
        attr_class = get_type_class(attr_type)
        if attr_class == "EventDataDetails":
            continue
        if attr_num > 0:
            class_str += f"{tab}(\"{attr_name}\", {attr_class} * {attr_num}),\n"
            continue
        class_str += f"{tab}(\"{attr_name}\", {attr_class}),\n"
    tab = tab[:-1]
    class_str += f"{tab}]\n"
    return class_str


PACKET_FORMAT = 2024
PACKET_VERSION = 1


def get_HEADER_FIELD_TO_PACKET_TYPE_str(spec_path: str):
    ret_str = "HEADER_FIELD_TO_PACKET_TYPE = {\n"
    tab = "\t"
    packet_ids_ = packet_ids.get(spec_path)
    for idx, name in packet_ids_.items():
        ret_str += f"{tab}({PACKET_FORMAT}, {PACKET_VERSION}, {idx}) : {name},\n"
    ret_str += "}\n"
    return ret_str


def get_PACKET_ID_TO_PACKET_TYPE_STR_str(spec_path: str):
    ret_str = "PACKET_ID_TO_PACKET_TYPE_STR = {\n"
    tab = "\t"
    packet_ids_ = packet_ids.get(spec_path)
    for idx, name in packet_ids_.items():
        ret_str += f"{tab}{idx}: '{name}',\n"
    ret_str += "}\n"
    return ret_str


if __name__ == '__main__':
    spec_path = "./Data Output from F1 24 v27.2x.docx"
    path_template = os.path.join(os.path.dirname(__file__), "packets.py.templ")
    path_out = "./packets.py"
    with open(path_out, 'w') as f:
        with open(path_template, 'r') as f_templ:
            templ_text = f_templ.read()
        f.write(templ_text + "\n\n")

    text = get_str_from_doc(spec_path)
    structs = get_structs(text)

    for struct in structs:
        class_str = get_class_str_from_struct_text(struct)
        with open(path_out, 'a') as f:
            f.write(class_str + "\n\n")

    header_field_to_packet_type_str = get_HEADER_FIELD_TO_PACKET_TYPE_str(
        spec_path)
    with open(path_out, 'a') as f:
        f.write(header_field_to_packet_type_str + "\n")

    with open(path_out, 'a') as f:
        f.write(get_PACKET_ID_TO_PACKET_TYPE_STR_str(spec_path))
