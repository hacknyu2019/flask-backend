import os
import re
import json
import pprint
import PyPDF2

from flask import Flask, jsonify, request, redirect, abort

# from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './pdf/'
app = Flask(__name__)


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/")
def hello_word():
    return "Hello World!"


@app.route("/upload", methods=['POST'])
def upload_pdf():
    file = request.files['file']
    # submit an empty part without filename
    if file.filename == '':
        # flash('No selected file')
        abort(404)
    if file:
        filename = re.sub(' ', '', file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    pdfFileObj = open(os.path.join(UPLOAD_FOLDER, filename), 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

    num_pages = pdfReader.numPages
    print(num_pages)
    count = 0
    text_arr = []
    while count < num_pages:
        page = pdfReader.getPage(count)
        count += 1
        page_text = page.extractText()
        text_arr.append(page_text)

    return json.dumps(text_arr)


if __name__ == "__main__":
    port = os.getenv('PORT', '5000')
    app.run(debug=True, host='0.0.0.0', port=int(port))
