from watson_developer_cloud import NaturalLanguageUnderstandingV1
import watson_developer_cloud.natural_language_understanding.features.v1 \
    as Features

API_KEY = 'XSEYce5PdhtoYy64ENJM5ioOcwjNLeMRx-XpZ3IEVUGq'

natural_language_understanding = NaturalLanguageUnderstandingV1(
    iam_apikey=API_KEY,
    version="2017-02-27")

response = natural_language_understanding.analyze(
    text="IBM has one of the largest workforces in the world",
    features=[
        Features.Concepts(
            # Concepts options
            limit=50
        ),
        Features.Keywords(
            # Keywords options
            # sentiment=True,
            # emotion=True,
            limit=10
        )
    ]
)

print(response.text)

