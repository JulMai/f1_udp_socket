from utils.doc.appendices.tables import get_table_from_doc, get_table_content, TABLE_IDX_23


def get(file_path: str):
    id = TABLE_IDX_23["InfringementTypes"]
    table = get_table_from_doc(file_path, id)
    infringement_types = get_table_content(table, "Infringement meaning")
    return infringement_types


if __name__ == '__main__':
    path = ""
    infringement_types = get(path)
    print()
