import json
import requests
from PIL import Image
import base64


def convert(json_image):
    json_image = json.loads(json_image)
    file = json_image['file']
    file_name = json_image['file_name']

    with open(file_name, "wb") as f:
        f.write(base64.b64decode(file))
    image = Image.open(file_name).convert('L')
    image.save(file_name)

    with open(file_name, 'rb') as f:
        file = f.read()
        file = base64.b64encode(file).decode('utf-8')
        result_dict = dict(file_name=file_name, file=file)
        requests.post(" http://server", json=result_dict)