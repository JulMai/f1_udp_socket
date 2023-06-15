import os
import importlib.util


def get(path: str, spec_path: str):
    appendices = {}
    for filename in os.listdir(path):
        if filename.endswith('.py'):
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


def write(path: str, appendices: dict):
    with open(path, 'w') as f:
        for name, value in appendices.items():
            f.write(f"{name} = {value}\n\n")


if __name__ == '__main__':
    appendices_path = os.path.join("src", "utils", "doc", "appendices")
    spec_path = "C:\\Users\\julia\\Downloads\\Data Output from F1 22 v16.docx"
    path_to = os.path.join(".", "data", "appendices.py")
    dicts = get(appendices_path, spec_path)
    write(path_to, dicts)
