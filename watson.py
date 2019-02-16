from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions, ConceptsOptions, CategoriesOptions

API_KEY = 'XSEYce5PdhtoYy64ENJM5ioOcwjNLeMRx-XpZ3IEVUGq'


def ibm_nlp(text_input):
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version="2017-02-27",
        iam_apikey=API_KEY)

    response = natural_language_understanding.analyze(
        text=text_input,
        features=Features(concepts=ConceptsOptions(),
                          entities=EntitiesOptions(),
                          keywords=KeywordsOptions(),
                          categories=CategoriesOptions())).get_result()
    return response
