import os
import json

from flask.json import jsonify
from watson_developer_cloud import DiscoveryV1

API_KEY = os.environ.get('IBM_DISCOVERY_API_KEY')

news_cache = {}


def get_news(query):
    if news_cache.__contains__(query):
        print("found news in cache")
        return news_cache.get(query)

    discovery = DiscoveryV1(
        iam_apikey=API_KEY,
        version='2017-08-01'
    )
    environments = discovery.list_environments().get_result()
    # print(json.dumps(environments, indent=2))

    #  if x['name'] == 'Watson Discovery News Environment'
    news_environments = [x for x in environments['environments']]
    # print(json.dumps(news_environments, indent=2))
    news_environment_id = news_environments[0]['environment_id']

    collections = discovery.list_collections(news_environment_id).get_result()
    # print(json.dumps(collections, indent=2))
    news_collections = [x for x in collections['collections']]

    results = discovery.query(count=5, return_fields=['title, text, url, sentiments'],
                              environment_id=news_environment_id,
                              collection_id='news-en', query=query).get_result()

    news_cache[query] = str(results)

    return results


if __name__ == '__main__':
    print(get_news("test sentence with computer networks"))
