import os
import re
import json
from pprint import pprint
import PyPDF2

from flask import Flask, jsonify, request, redirect, abort

# from werkzeug.utils import secure_filename
from news import get_news
from watson import get_concepts

UPLOAD_FOLDER = './pdf/'
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/process_pdf", methods=['POST'])
def process_pdf():
    page_num = request.args['page']
    print(page_num)
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
    count = 0
    text_arr = []
    # while count < num_pages:
    page = pdfReader.getPage(int(page_num))
    # count += 1
    page_text = page.extractText()
    # pprint(get_concepts(page_text))
    # text_arr.append(page_text)

    news = nlp_process(page_text)

    return news


def nlp_process(text):
    concepts = []
    # for text in text_arr:
    concepts, entities = get_concepts(text)
    pprint(concepts)
    pprint(entities)
    print('_______________________')
    texts = [concept['text'] for concept in entities]
    # print(texts)
    query = " ".join(texts)
    news = get_news(query)
    pprint(news)
    return news


if __name__ == "__main__":
    port = os.getenv('PORT', '5000')
    app.run(debug=True, host='0.0.0.0', port=int(port))
