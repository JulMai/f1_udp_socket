from utils.doc.appendices.tables import get_table_from_doc, get_table_content, TABLE_IDX_23

def get(file_path: str):
    id = TABLE_IDX_23["RuleSetIDs"]
    table = get_table_from_doc(file_path, id)
    rulesets = get_table_content(table, "Team")
    return rulesets


if __name__ == '__main__':
    path = ""
    rulesets = get(path)
    print()