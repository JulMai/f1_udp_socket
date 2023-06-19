from utils.doc.appendices.tables import get_table_from_doc, get_table_content, TABLE_IDX_23

def get(file_path: str):
    id = TABLE_IDX_23["SurfaceTypes"]
    table = get_table_from_doc(file_path, id)
    surface_types = get_table_content(table, "Surface")
    return surface_types


if __name__ == '__main__':
    path = ""
    surface_types = get(path)
    print()