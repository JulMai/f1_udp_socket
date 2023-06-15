from utils.doc.appendices.tables import get_table_from_doc, get_table_keys, TABLE_IDX_23


def get(file_path: str):
    id = TABLE_IDX_23["PacketIDs"]
    table = get_table_from_doc(file_path, id)
    packet_ids = get_table_content(table, "Packet Name")
    return packet_ids


def get_table_content(table, value_key: str):
    values = {}
    keys = get_table_keys(table)

    id = ""
    value = ""

    for i, row in enumerate(table.rows):
        for j, cell in enumerate(row.cells):
            text = cell.text
            if "‘" in text:
                text = text.replace("‘", "`")
            if text == '\xa0' or text == '':
                continue
            if text == "Value" or text == value_key:
                continue
            if keys[j] == "Value":
                id = int(text)
            elif keys[j] == value_key:
                value = text.replace(" ", "")
                value = f"Packet{value}Data"
            if id != "" and value != "":
                values[id] = value
                id = ""
                value = ""

    values = dict(sorted(values.items(), key=lambda x: x[0]))
    return values


if __name__ == '__main__':
    path = ""
    packet_ids = get(path)
    print()
