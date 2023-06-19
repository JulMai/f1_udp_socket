from utils.doc.appendices.tables import get_table_from_doc, get_table_content, TABLE_IDX_23

def get(file_path: str):
    id = TABLE_IDX_23["GameModeIDs"]
    table = get_table_from_doc(file_path, id)
    gamemodes = get_table_content(table, "Mode")
    return gamemodes


if __name__ == '__main__':
    path = ""
    gamemodes = get(path)
    print()