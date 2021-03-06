import json
import os
from pprint import pprint

import requests

JWT = os.environ.get('JWT')


HEADERS = {
    'Accept': 'application/json',
    'Content-type': 'application/json',
    'Authorization': 'Bearer ' + JWT
}

agolo_cache = {}


def get_summarization_request_payload(articles):
    return {
        'articles': articles,
        'summary_length': 3
    }


def get_agolo_summary(article_url):
    global agolo_cache
    if agolo_cache.__contains__(article_url):
        print("Found summary in cache")
        return agolo_cache.get(article_url)

    articles = [{'url': article_url}]
    response = requests.post('http://summarization-api.prod.agolo.com/summarization-api-java-0.2.0/v0.2/summarize',
                             data=json.dumps(get_summarization_request_payload(articles)),
                             headers=HEADERS, verify=False)
    pprint(json.loads(response.text)['summary'])
    if response.text is not None and response.text != '' \
            and json.loads(response.text)['summary']:
        agolo_cache[article_url] = json.loads(response.text)['title'], \
                                   json.loads(response.text)['summary'][0]['sentences']
        return json.loads(response.text)['title'], \
               json.loads(response.text)['summary'][0]['sentences'],

    return '', []


# if __name__ == '__main__':
#     print(get_agolo_summary(
#         "http://community.energycentral.com/c/ec/green-new-deal-can%E2%80%99t-be-concocted-out-hot-air"))
