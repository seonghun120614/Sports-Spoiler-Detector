from src.services.models.NER import GliNER

from tests.services.constants import TITLE_EX


def test_ner():
    model = GliNER()

    results = model.extract(TITLE_EX)

    print(results)