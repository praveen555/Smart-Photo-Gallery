# Clear S3 and dynamo DB data
import json

import boto3
import requests
from flask import render_template
from app.connector import bucket, aws_access_key_id, aws_secret_access_key, region_name
from app import webapp


@webapp.route('/clear_data', methods=['GET'])
def clear_data():
    delete_s3()
    delete_dynamo()
    delete_opensearch()

    return render_template('clear_data.html')


def delete_s3():
    s3 = boto3.resource('s3',
                        aws_access_key_id=aws_access_key_id,
                        aws_secret_access_key=aws_secret_access_key,
                        region_name=region_name)
    s3bucket = s3.Bucket(bucket)
    response = s3bucket.objects.all().delete()

    print(str(response))


def delete_dynamo():
    dynamodb = boto3.client('dynamodb',
                            aws_access_key_id=aws_access_key_id,
                            aws_secret_access_key=aws_secret_access_key,
                            region_name=region_name)

    table_name = 'a3-images'

    response = dynamodb.scan(
        TableName=table_name,
        AttributesToGet=[
            'key',
            'image'
        ])
    all_items = []
    for item in response['Items']:
        single_item = {'key': item['key']}
        all_items.append(single_item)

    keys = all_items

    for key in keys:
        print("keys", key)
        response = dynamodb.delete_item(
            TableName=table_name,
            Key=key)
        print(response)
    else:
        print("DynamoDB already empty")


def delete_opensearch():
    # Delete index
    DeleteEndpoint = 'https://search-photo-gallery-bumzzdzztuk5upjw7g6cslniie.us-east-1.es.amazonaws.com/photo-gallery'
    esauth = ('Master', 'Master@123')
    headers = {"Content-Type": "application/json"}
    response = requests.delete(DeleteEndpoint, auth=esauth, headers=headers)
    res = response.json()
    print(res)

    # Create index
    body = {
        "settings": {
            "number_of_shards": 5,
            "number_of_replicas": 1
        }
    }
    CreateIndexEndpoint = "https://search-photo-gallery-bumzzdzztuk5upjw7g6cslniie.us-east-1.es.amazonaws.com/photo-gallery"
    esauth = ('Master', 'Master@123')
    headers = {"Content-Type": "application/json"}
    response = requests.put(CreateIndexEndpoint, auth=esauth, data=json.dumps(body).encode("utf-8"), headers=headers)
    res = response.json()
    print(res)
