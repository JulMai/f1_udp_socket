from utils.doc.appendices.tables import get_table_from_doc, get_table_keys, TABLE_IDX_23

def get(file_path: str):
    id = TABLE_IDX_23["ButtonFlags"]
    table = get_table_from_doc(file_path, id)
    button_flags = get_table_content(table, "Button")
    return button_flags

def get_table_content(table, value_key: str):
    values = {}
    keys = get_table_keys(table)

    id = ""
    value = ""

    for i, row in enumerate(table.rows):
        for j, cell in enumerate(row.cells):
            text = cell.text
            if text == '\xa0' or text == '':
                continue
            if text == "Bit Flag" or text == value_key:
                continue
            if keys[j] == "Bit Flag":
                id = text
            elif keys[j] == value_key:
                value = text
            if id != "" and value != "":
                values[id] = value
                id = ""
                value = ""

    values = dict(sorted(values.items(), key=lambda x: x[0]))
    return values


if __name__ == '__main__':
    path = ""
    button_flags = get(path)
    print()