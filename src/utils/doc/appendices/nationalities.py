from utils.doc.appendices.tables import get_table_from_doc, get_table_content, TABLE_IDX_23

def get(file_path: str):
    id = TABLE_IDX_23["NationalityIDs"]
    table = get_table_from_doc(file_path, id)
    nationalities = get_table_content(table, "Nationality")
    return nationalities


if __name__ == '__main__':
    path = ""
    nationalities = get(path)
    print()