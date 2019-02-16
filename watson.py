import os
from pprint import pprint

from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, \
    EntitiesOptions, KeywordsOptions, ConceptsOptions, CategoriesOptions

API_KEY = os.environ.get('IBM_API_KEY')


def get_concepts(text_input):
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version="2017-02-27",
        iam_apikey=API_KEY)

    try:
        response = natural_language_understanding.analyze(
            text=text_input,
            features=Features(concepts=ConceptsOptions(),
                              # entities=EntitiesOptions(),
                              # keywords=KeywordsOptions(),
                              # categories=CategoriesOptions()
                              )).get_result()
        return response['concepts']
    except Exception as e:
        print("Could not get concepts for this page", text_input)
        return None


if __name__ == '__main__':
    pprint(get_concepts("Sample Test data sentence "))
