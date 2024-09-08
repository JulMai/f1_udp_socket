import os
import importlib.util


def get(path: str, spec_path: str):
    appendices = {}
    for filename in os.listdir(path):
        if filename.endswith('.py') and not "tables" in filename:
            module_name = filename[:-3]
            module_path = os.path.join(path, filename)

            spec = importlib.util.spec_from_file_location(
                module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            if hasattr(module, 'get'):
                result = module.get(spec_path)
                appendices[module_name.upper()] = result
    return appendices

def get_header() -> str:
    path = os.path.join("src", "write", "header.txt")
    with open(path) as f:
        content = f.read()
    return content

def format_dict(dict) -> str:
    string = "{\n"
    tab = "\t"
    for key, value in dict.items():
        if type(key) is int:
            string += f"{tab}{key} : '{value}',\n"
            continue
        string += f"{tab}'{key}' : '{value}',\n"
    tab = tab[:-1]
    string += "}"
    return string


def write(path: str, appendices: dict, header: str):
    with open(path, 'w') as f:
        f.write(header + "\n\n")
        for name, value in appendices.items():
            formatted_value = format_dict(value)
            f.write(f"{name} = {formatted_value}\n\n")


if __name__ == '__main__':
    appendices_path = os.path.join("src", "utils", "doc", "appendices")
    spec_path = ".\\Data Output from F1 24 v27.2x.docx"
    path_to = os.path.join(".", "data", "appendices.py")
    dicts = get(appendices_path, spec_path)
    header = get_header()
    write(path_to, dicts, header)
