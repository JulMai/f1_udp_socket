from utils.doc.appendices.tables import get_table_from_doc, get_table_content, TABLE_IDX_23


def get(file_path: str):
    table_id = TABLE_IDX_23["TrackIDs"]
    table = get_table_from_doc(file_path, table_id)
    tracks = get_table_content(table, "Track")
    return tracks


if __name__ == "__main__":
    path = ""
    tracks = get(path)
    print()