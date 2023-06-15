import zipfile
import re

def get_str_from_doc(path: str):
    docx = zipfile.ZipFile(path)
    content = docx.read('word/document.xml').decode('utf-8')
    cleaned = re.sub('<(.|n)*?>', '', content)
    return cleaned