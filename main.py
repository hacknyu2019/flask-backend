import os
import re
import json
import pprint
import PyPDF2

from flask import Flask, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './pdf/'
app = Flask(__name__)


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def hello_word():
    return "Hello World!"

@app.route("/upload", methods=['POST'])
def upload_pdf():
    test = request.files
    file = request.files['file']
    # submit an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file:
        # filename = secure_filename(file.filename)
        filename = re.sub(' ', '', file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # return redirect(url_for('upload_pdf',
        #                         filename=filename))

    
    print(file.filename)
    print(type(file.filename))
    # pdfFileObj = filename.read()
    # print(pdfFileObj)
    pdfFileObj = open(os.path.join(UPLOAD_FOLDER, filename), 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

    num_pages = pdfReader.numPages
    count = 0
    text_arr = []
    # The while loop will read each page
    while count < num_pages:
        pageObj = pdfReader.getPage(count)
        count +=1
        encoded_text = "".join(map(chr, pageObj.extractText().encode('UTF-8')))
        print(encoded_text)
        text_arr.append(pageObj.extractText().encode('UTF-8'))
    final = "".join(map(chr, text_arr))
    print(final)
    print(count)
    print(text_arr)
    

    return jsonify(results=text_arr)
    # return 1


port = os.getenv('PORT', '5000')
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(port))