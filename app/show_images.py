import json

import boto3
import requests
from flask import render_template, request

from app import webapp


@webapp.route('/all-images', methods=['GET', 'POST'])
def all_images():
    query = {
        "query": {
            "match_all": {}
        }
    }
    openSearchEndpoint = 'https://search-photo-gallery-bumzzdzztuk5upjw7g6cslniie.us-east-1.es.amazonaws.com/photo-gallery/_search'
    esauth = ('Master', 'Master@123')
    headers = {"Content-Type": "application/json"}
    response = requests.post(openSearchEndpoint, auth=esauth, data=json.dumps(query).encode("utf-8"), headers=headers)
    res = response.json()
    image_list = []
    if len(res['hits']['hits']) > 0:
        data = res['hits']['hits']
        data = [item['_source'] for item in data]

        for im in data:
            image = {'key': im['key'], 'image': dynamo_get_imagename(im['key']), 'labels': im['labels']}
            image_list.append(image)

        print("image_list", image_list)
        return render_template('all_images.html', images=image_list, len=1)
    else:
        return render_template('all_images.html', images=image_list, len=0)


# @webapp.route('/images', methods=['GET', 'POST'])
# def images():
#     sentence = request.values.get('search')
#     print(sentence)
#     query = lex_query_to_label(sentence)
#     # image_list = get_items(query)
#     image_list = []
#     print(image_list)
#     return render_template('images.html', query=query, images=image_list)


@webapp.route('/search', methods=['GET', 'POST'])
def search():
    transcription = request.values.get('search')
    # print("Flask received:", transcription)
    transcription = transcription.replace(".", "")
    print("Searching for:", transcription)
    query = lex_query_to_label(transcription)  # second item implementation is left.
    # image_list = []
    print("Item:", query, "\n--------------------")
    image_list = elastic_search(transcription)
    # image_list = get_items(query[0])
    print("Displaying:", image_list)

    return render_template('images.html', query=query[0].capitalize(), images=image_list, len=len(image_list))


def lex_query_to_label(query):
    aws_access_key = "AKIAQGOWDODFP7S4CA4T"
    aws_secret_access_key = "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"
    region_name = "us-east-1"
    lex = boto3.client('lex-runtime',
                       aws_access_key_id=aws_access_key,
                       aws_secret_access_key=aws_secret_access_key,
                       region_name=region_name)

    lex_res = lex.post_text(
        botName='search_bot_karl',
        botAlias='$LATEST',
        userId='user0',
        inputText=query
    )

    # print(lex_res)
    obj1 = lex_res["slots"]["object_one"]
    obj1 = obj1.lower() if obj1 else ''
    obj2 = lex_res["slots"]["object_two"]
    obj2 = obj2.lower() if obj2 else ''
    # print("Obj1", obj1, "  Obj2", obj2)
    return obj1, obj2


def elastic_search(query):
    obj1, obj2 = lex_query_to_label(query)
    query = {
        "size": 20,
        "query": {
            "dis_max": {
                "queries":
                    [{
                        "multi_match": {
                            "query": obj1,
                            "fields": ["labels"]
                        }
                    },
                        {
                            "multi_match": {
                                "query": obj2,
                                "fields": ["labels"]
                            }
                        }]
            }
        }
    }

    openSearchEndpoint = 'https://search-photo-gallery-bumzzdzztuk5upjw7g6cslniie.us-east-1.es.amazonaws.com/photo-gallery/_search'
    esauth = ('Master', 'Master@123')
    headers = {"Content-Type": "application/json"}
    response = requests.post(openSearchEndpoint, auth=esauth, data=json.dumps(query).encode("utf-8"), headers=headers)
    res = response.json()
    # print(res)
    data = {}
    if len(res['hits']['hits']) > 0:
        data = res['hits']['hits']
        data = [item['_source'] for item in data]

    imagename_list = []
    for item in data:
        # print("Key:", item['key'])
        imagename_list.append(dynamo_get_imagename(item['key']))

    return imagename_list


def dynamo_get_imagename(key):
    aws_access_key = "AKIAQGOWDODFP7S4CA4T"
    aws_secret_access_key = "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"
    region_name = "us-east-1"

    dynamodb = boto3.client('dynamodb',
                            aws_access_key_id=aws_access_key,
                            aws_secret_access_key=aws_secret_access_key,
                            region_name=region_name)

    table_name = 'a3-images'

    response = dynamodb.get_item(
        TableName=table_name,
        Key={
            'key': {'S': key},
        }
    )

    if 'Item' in response:
        if 'image' in response['Item']:
            if 'S' in response['Item']['image']:
                # print("Image:", response['Item']['image']['S'], "\n--------------------")
                return response['Item']['image']['S']

    return ""
