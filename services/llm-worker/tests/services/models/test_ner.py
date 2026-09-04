from src.services.models.NER import GliNER

from tests.services.constants import TITLE_EX


def test_ner():
    model = GliNER()

    results = model.predict([TITLE_EX, "HELLO"])

    print(results)