from utils.doc.appendices.tables import get_table_from_doc, get_table_content, TABLE_IDX_23


def get(file_path: str) -> dict:
    id = TABLE_IDX_23["TeamIDs"]
    table = get_table_from_doc(file_path, id)
    teams = get_table_content(table, "Team")
    return teams


if __name__ == "__main__":
    path = ""
    teams = get(path)
    print()
