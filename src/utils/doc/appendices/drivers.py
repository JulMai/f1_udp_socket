from utils.doc.appendices.tables import get_table_from_doc, get_table_content, TABLE_IDX_23

def get(file_path: str):
    id = TABLE_IDX_23["DriverIDs"]
    table = get_table_from_doc(file_path, id)
    drivers = get_table_content(table, "Driver")
    return drivers


if __name__ == '__main__':
    path = ""
    drivers = get(path)
    print()