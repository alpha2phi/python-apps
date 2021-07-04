import boto3
import json

endpoint = 'yolo-v32021'

runtime = boto3.Session().client('sagemaker-runtime')

with open("images/test.jpg", 'rb') as f:
    payload = f.read()

response = runtime.invoke_endpoint(EndpointName=endpoint,
                                   ContentType='image/jpeg',
                                   Accept='image/jpeg',
                                   Body=payload)

result = json.loads(response['Body'].read().decode())
print(result)
