import os
from flask import Flask, request, render_template
from pypdf import PdfReader
import json
from resumeparser import ats_extractor

# Set up the Flask app
UPLOAD_PATH = r"__DATA__"
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/process", methods=["POST"])
def ats():
    # Save uploaded PDF file
    doc = request.files['pdf_doc']
    doc.save(os.path.join(UPLOAD_PATH, "file.pdf"))
    doc_path = os.path.join(UPLOAD_PATH, "file.pdf")

    # Read the content from the saved PDF file
    data = _read_file_from_path(doc_path)

    # Extract ATS data using the ats_extractor function
    extracted_data = ats_extractor(data)
    print("extracted Data:", extracted_data)

    # Ensure extracted_data is a valid JSON string before loading
    

    # Render the index page with the extracted data
    return render_template('index.html', data=extracted_data)

def _read_file_from_path(path):
    reader = PdfReader(path)
    data = ""

    # Extract text from each page of the PDF
    for page_no in range(len(reader.pages)):
        page = reader.pages[page_no]
        data += page.extract_text()

    return data

if __name__ == "__main__":
    app.run(port=8000, debug=True)
