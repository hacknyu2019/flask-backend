import json
from pprint import pprint

import requests

HEADERS = {
    'Accept': 'application/json',
    'Content-type': 'application/json',
    # 'Authorization': 'Bearer ' + JWT
}


def get_summarization_request_payload(articles):
    return {
        'articles': articles,
        'summary_length': 3
    }


def get_agolo_summary(article_url):
    articles = [{'url': article_url}]
    response = requests.post('https://node-sum.staging.agolo.com/summarization',
                             data=json.dumps(get_summarization_request_payload(articles)),
                             headers=HEADERS, verify=False)
    pprint(response.text)
    return json.loads(response.text)['title'], json.loads(response.text)['sentences']


if __name__ == '__main__':
    print(get_agolo_summary(
        "http://community.energycentral.com/c/ec/green-new-deal-can%E2%80%99t-be-concocted-out-hot-air"))
