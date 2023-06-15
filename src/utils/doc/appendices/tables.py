from docx import Document


def get_table_from_doc(file_path: str, id: int):
    document = Document(file_path)
    table = document.tables[id]
    return table


def get_table_keys(table) -> dict:
    row = table.rows[0]
    keys = {}
    for i, cell in enumerate(row.cells):
        keys[i] = cell.text
        i += 1
    return keys


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
            if text == "ID" or text == value_key:
                continue
            if keys[j] == "ID":
                id = int(text)
            elif keys[j] == value_key:
                value = text
            if id != "" and value != "":
                values[id] = value
                id = ""
                value = ""

    values = dict(sorted(values.items(), key=lambda x: x[0]))
    return values


TABLE_IDX_23 = {
    "PacktTypes": 0,
    "PacketIDs": 1,
    "EventStringCodes": 2,
    "TeamIDs": 3,
    "DriverIDs": 4,
    "TrackIDs": 5,
    "NationalityIDs": 6,
    "GameModeIDs": 7,
    "RuleSetIDs": 8,
    "SurfaceTypes": 9,
    "ButtonFlags": 10,
    "PenaltyTypes": 11,
    "InfringementTypes": 12
}
