from src.services.models.TextClassifier import SetFitImpl

from tests.services.constants import *

def test_set_fit_impl():
    model = SetFitImpl()

    results = model.predict([TITLE_EX, "1:0 한국 역전승"])

    print(results)