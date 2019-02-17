import os
import shelve
import threading
import uuid
import json
from multiprocessing.pool import ThreadPool

import requests
from pprint import pprint
import PyPDF2
import requests
import urllib3

from flask import Flask, jsonify, request, abort

from flask_cors import CORS

from agolo import get_agolo_summary
from news import get_news
from watson import get_concepts

urllib3.disable_warnings()

UPLOAD_FOLDER = './pdf/'
app = Flask(__name__)
CORS(app)
import multiprocessing

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

pdf_cache = {}


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
        file.close()
        return jsonify({'id': new_uuid})


@app.route("/process_pdf")
def process_pdf():
    page_num = request.args['page']
    id = request.args['id']

    print(pdf_cache.get(str(id) + str(page_num)))

    if pdf_cache.__contains__(str(id) + str(page_num)):
        return pdf_cache.get(str(id) + str(page_num))

    pdfFileObj = open(os.path.join(UPLOAD_FOLDER, id + '.pdf'), 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    if pdfReader.isEncrypted:
        pdfReader.decrypt('')

    page = pdfReader.getPage(int(page_num))
    page_text = page.extractText()

    pool = multiprocessing.Pool(processes=4)

    concepts, entities = get_concepts(page_text)
    print('Got concepts')
    news = pool.apply_async(get_news_summaries, args=(concepts,)).get()
    definitions = pool.apply_async(get_definitions, args=(concepts,)).get()

    final_resp = {'definitions': definitions, 'news': news}

    pdf_cache[str(id) + str(page_num)] = jsonify(final_resp)

    return jsonify(final_resp)


def get_definitions(concepts):
    texts = [concept['text'] for concept in concepts]
    links = [concept['dbpedia_resource'] for concept in concepts]
    all_concept_info = []

    definition_count = 0
    # print(len(texts))
    if len(texts) > 5 and definition_count < 5:
        definition_count += 1
        for word in range(len(texts)):
            r = requests.get('https://en.wikipedia.org/api/rest_v1/page/summary/' + texts[word])
            content = json.loads(r.text)
            if 'extract' in content:
                all_concept_info.append({'title': texts[word], 'url': links[word], 'text': content['extract']})
    if len(texts) <= 5:
        for word in range(len(texts)):
            r = requests.get('https://en.wikipedia.org/api/rest_v1/page/summary/' + texts[word])
            content = json.loads(r.text)
            if 'extract' in content:
                all_concept_info.append({'title': texts[word], 'url': links[word], 'text': content['extract']})

    return all_concept_info


def get_news_summaries(concepts):
    # concepts, entities = get_concepts(text)
    # pprint(concepts)
    texts = [concept['text'] for concept in concepts]
    # print(texts)
    query = " ".join(texts)
    news = get_news(query)['results']

    print("Got news, summarizing")
    news_summaries = []
    for news_article in news:
        news_article['title'], news_article['text'] = get_agolo_summary(news_article['url'])
        if news_article['title']:
            news_summaries.append(news_article)

    print("Got summaries")

    print('----------------------')

    return news_summaries


if __name__ == "__main__":
    port = os.getenv('PORT', '5000')
    app.run(debug=False, host='0.0.0.0', port=int(port))
