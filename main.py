import os
import uuid
import json
import requests
from pprint import pprint
import PyPDF2

from flask import Flask, jsonify, request, abort

from flask_cors import CORS

from news import get_news
from watson import get_concepts

UPLOAD_FOLDER = './pdf/'
app = Flask(__name__)
CORS(app)


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/upload", methods=['POST'])
def upload():
    file = request.files['file']

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    if file.filename == '':
        # flash('No selected file')
        abort(404)
    if file:
        new_uuid = str(uuid.uuid4())
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_uuid + '.pdf'))
        return jsonify({'id': new_uuid})


@app.route("/process_pdf")
def process_pdf():
    page_num = request.args['page']
    id = request.args['id']

    pdfFileObj = open(os.path.join(UPLOAD_FOLDER, id + '.pdf'), 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    if pdfReader.isEncrypted:
        pdfReader.decrypt('')

    page = pdfReader.getPage(int(page_num))
    page_text = page.extractText()

    news = nlp_process(page_text)

    definitions = concepts_process(page_text)

    final_resp = {'definitions': definitions, 'news': news}

    return jsonify(final_resp)


def concepts_process(text):
    concepts, entities = get_concepts(text)
    texts = [concept['text'] for concept in concepts]
    links = [concept['dbpedia_resource'] for concept in concepts]
    all_concept_info = []

    for word in range(len(texts)):
        r = requests.get('https://en.wikipedia.org/api/rest_v1/page/summary/' + texts[word])
        content = json.loads(r.text)
        if 'extract' in content:
            all_concept_info.append({'text': texts[word], 'url': links[word], 'description': content['extract']})

    return all_concept_info

def nlp_process(text):
    concepts, entities = get_concepts(text)
    pprint(concepts)
    pprint(entities)
    print('_______________________')
    texts = [concept['text'] for concept in entities]

    query = " ".join(texts)
    news = get_news(query)
    pprint(news)

    return news


if __name__ == "__main__":
    with app.app_context():
        port = os.getenv('PORT', '5000')
        app.run(debug=False, host='0.0.0.0', port=int(port))
