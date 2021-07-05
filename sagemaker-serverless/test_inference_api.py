import json
import base64
import requests

API_URL = "https://aeab47j4z7.execute-api.ap-southeast-1.amazonaws.com/prod/inference"

payload = ""
with open("images/test.jpg", 'rb') as f:
    payload = f.read()

payload = base64.encodebytes(payload).decode("utf-8")

data = {"data": payload}

response = requests.post(API_URL, data=json.dumps(data))
print(json.loads(response.text))
