import json

import boto3
import numpy as np
import pandas as pd

endpoint = 'sagemaker-xgboost-2021-06-27-13-29-55-164'

runtime = boto3.Session().client('sagemaker-runtime')

# Read test data into dataframe
df = pd.read_csv("test_data/test_data.csv")
test_df = df.drop(["y_no", "y_yes"], axis=1)
test_df.to_csv("test_data/test_data_cleaned.csv", index=False, header=False)

predictions = ""
with open("test_data/test_data_cleaned.csv") as f:
    for _, line in enumerate(f):
        response = runtime.invoke_endpoint(
            EndpointName=endpoint, ContentType='csv', Body=line,
            Accept='Accept')
        prediction = response['Body'].read().decode("utf-8")[0]
        predictions = ",".join([predictions, prediction])

print(predictions)
