from django.test import TestCase
import boto3
import sagemaker

# Create your tests here.

client = boto3.client('sagemaker')

boto_session = boto3.Session(region_name = "us-east-2")
#sess = sagemaker.Session(boto_session = boto_session)
sess = sagemaker.Session(boto_session = boto_session, sagemaker_client=client, sagemaker_runtime_client=client)
endpoint_name = "911ATMA-20201026"
deployed_endpoint = sagemaker.predictor.RealTimePredictor(endpoint_name, sagemaker_session = sess)
print(deployed_endpoint)

client = boto3.client('dynamodb', region_name='us-east-2', aws_access_key_id="AKIATIGBJSAAQH6C3RHY", aws_secret_access_key="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")
response = client.list_tables()
print(response)