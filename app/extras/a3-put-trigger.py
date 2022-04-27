import json
import urllib.parse
import boto3
import logging
import os
import time

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client('s3')


def put_items(labels, image, confidence):
    # aws_access_key = os.environ.get('AWS_ACCESS_KEY')
    # aws_secret_access_key = os.environ.get(' AWS_SECRET_ACCESS_KEY')
    labels = labels.lower()
    aws_access_key = "AKIAQGOWDODFP7S4CA4T"
    aws_secret_access_key = "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"

    region_name = "us-east-1"

    dynamodb = boto3.client('dynamodb',
                            aws_access_key_id=aws_access_key,
                            aws_secret_access_key=aws_secret_access_key,
                            region_name=region_name)

    table_name = 'a3-imagelabels'

    item = {
        'label': {'S': labels},
        'image_path': {'S': image},
        'confidence': {'S': confidence}
    }
    response = dynamodb.put_item(
        TableName=table_name,
        Item=item
    )
    print("Writing: " + labels + " " + image + " " + confidence)
    logger.info(str("Writing: " + labels + " " + image + " " + confidence))


def lambda_handler(event, context):
    # print("Received event: " + json.dumps(event, indent=2))
    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')

    aws_access_key = os.environ.get('AWS_ACCESS_KEY')
    aws_secret_access_key = os.environ.get(' AWS_SECRET_ACCESS_KEY')
    region_name = "us-east-1"

    metadata_label, metadata_confidence = [], []
    client = boto3.client('rekognition',
                          aws_access_key_id=aws_access_key,
                          aws_secret_access_key=aws_secret_access_key,
                          region_name=region_name)

    response = client.detect_labels(Image={'S3Object': {'Bucket': bucket, 'Name': key}}, MaxLabels=7)

    for label in response['Labels']:
        # print("Label: " + label['Name'])
        # print("Confidence: " + str(label['Confidence']))
        # Store in lists to display at front end also
        metadata_label.append(label['Name'])
        # label_confidence = format(label['Confidence'], '.2f')
        label_confidence = str(label['Confidence'])
        metadata_confidence.append(label_confidence)

        image_path = key.split("/")
        image_path = image_path[len(image_path) - 1]
        put_items(label['Name'], image_path, label_confidence)

    data = dict(zip(metadata_label, metadata_confidence))
    logger.info(str(data))
    print(str(data))

    # for label in metadata_label:
    #     get_items()
    #     put_items()
    openSearchEndpoint = 'https://search-smart-photo-album-ac9137-4urj6wdtjfde7va357525733be.us-east-1.es.amazonaws.com/photo_index/_doc/'
    esauth = ('Master', 'Master@123')
    format = {'objectKey': key, 'bucket': bucket, 'createdTimestamp': timestamp, 'labels': metadata_label}
    headers = {"Content-Type": "application/json"}
    r = requests.post(openSearchEndpoint, auth=esauth, data=json.dumps(format).encode("utf-8"), headers=headers)
    logger.info(r)
    logger.info(metadata_label)
