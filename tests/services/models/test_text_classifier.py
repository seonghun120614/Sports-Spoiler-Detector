from src.services.models.TextClassifier import SetFitImpl

from tests.services.constants import *

def test_set_fit_impl():
    model = SetFitImpl()

    results = model.extract(TITLE_EX)

    print(results)