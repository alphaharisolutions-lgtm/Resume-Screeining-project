import os
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'pdf', 'docx'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_resume(file, upload_folder):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        path = os.path.join(upload_folder, filename)
        file.save(path)
        return path
    return None

import docx
from pdfminer.high_level import extract_text as extract_pdf_text

def extract_text(file_path):
    ext = file_path.rsplit('.', 1)[1].lower()
    if ext == 'pdf':
        return extract_pdf_text(file_path)
    elif ext == 'docx':
        doc = docx.Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    return ""
