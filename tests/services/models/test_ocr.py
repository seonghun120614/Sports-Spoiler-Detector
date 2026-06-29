from src.services.models import EasyOCR

from tests.services.constants import IMAGE_URL_EX

from PIL import Image

import numpy as np
import requests

def test_ocr():
    model = EasyOCR()

    image = Image.open(requests.get(IMAGE_URL_EX, stream=True).raw).convert('RGB')

    image_arr = np.array(image)

    result = model.extract(image_arr)
    print(result)