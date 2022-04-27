import boto3
from datetime import datetime

# table_name = 'a2-images'


# def put_item(labels, image):
#     item = {
#         'label': {'S': labels},
#         'images': {'S': image}
#     }
#     print(item)
#     response = dynamodb.put_item(
#         TableName='a2-images',
#         Item=item
#     )
#     print("UPLOADING ITEM")
#     # print(response)
#
#
# def get_item(label):
#     response = dynamodb.query(
#         TableName=table_name,
#         KeyConditionExpression='label = :label',
#         ExpressionAttributeValues={
#             ':label': {'S': label}
#         }
#     )
#     if 'Item' in response:
#         print(response['Items'])
#     else:
#         print("No images of", label, "exist in the data.")
#     response = dynamodb.get_item(TableName='a2-images', Key={'label': {'S': label}})
#     if 'Item' in response:
#         print(response)
#     else:
#         print("No images of", label, "exist in the data.")
import requests


def put_items(labels, image):
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
        'status': {'BOOL': True}
    }
    print(item)
    response = dynamodb.put_item(
        TableName=table_name,
        Item=item
    )
    print("UPLOADED ITEM")
    # print(response)


def get_items(label):
    aws_access_key = "AKIAQGOWDODFP7S4CA4T"
    aws_secret_access_key = "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"
    region_name = "us-east-1"

    dynamodb = boto3.client('dynamodb',
                            aws_access_key_id=aws_access_key,
                            aws_secret_access_key=aws_secret_access_key,
                            region_name=region_name)

    table_name = 'a3-imagelabels'

    response = dynamodb.query(
        TableName=table_name,
        KeyConditionExpression='label = :label AND image_path < :image_path',
        ExpressionAttributeValues={
            ':label': {'S': label},
            ':image_path': {'S': 'zz'},
        }
    )
    images = []
    if 'Items' in response:
        # print("Label:", label)
        for image in response['Items']:
            # print(image)
            img_path = image['image_path']['S']
            images.append(img_path)
            # print(img_path)

        images = list(dict.fromkeys(images))
        return images
    else:
        print("No images of", label, "exist in the data.")
        return []


def delete_items(image):
    aws_access_key_id = "AKIAQGOWDODFP7S4CA4T"
    aws_secret_access_key = "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"
    region_name = "us-east-1"

    dynamodb = boto3.client('dynamodb',
                            aws_access_key_id=aws_access_key_id,
                            aws_secret_access_key=aws_secret_access_key,
                            region_name=region_name)

    table_name = 'a3-imagelabels'

    response = dynamodb.query(
        TableName=table_name,
        KeyConditionExpression='label < :label AND image_path = :image_path',
        ExpressionAttributeValues={
            ':label': {'S': 'zz'},
            ':image_path': {'S': image},
        }
    )
    images = []
    if 'Items' in response:
        # print("Label:", label)
        for item in response['Items']:
            # print(image)
            img_path = item['image_path']['S']
            images.append(img_path)
            print(img_path)

        images = list(dict.fromkeys(images))
        return images
    else:
        print("No images of", image, "exist in the data.")
        return []
    #
    # item = {
    #     'label': {'S': labels},
    #     'image_path': {'S': image},
    #     'status': {'BOOL': False}
    # }
    # print(item)
    # response = dynamodb.put_item(
    #     TableName=table_name,
    #     Item=item
    # )
    # print("DELETED ITEM")


def test():
    key = "images/5.jpg"
    image_path = key.split("/")
    print(image_path[len(image_path) - 1])


def scan():
    aws_access_key_id = "AKIAQGOWDODFP7S4CA4T"
    aws_secret_access_key = "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"
    region_name = "us-east-1"

    dynamodb = boto3.client('dynamodb',
                            aws_access_key_id=aws_access_key_id,
                            aws_secret_access_key=aws_secret_access_key,
                            region_name=region_name)

    table_name = 'a3-imagelabels'

    response = dynamodb.scan(
        TableName=table_name,
        AttributesToGet=[
            'label',
            'image_path'
        ])
    all_items = []
    # print(response)
    for item in response['Items']:
        single_item = {'image_path': item['image_path'], 'label': item['label']}
        all_items.append(single_item)

    # print(all_items)
    return all_items


def delete_all_items():
    aws_access_key = "AKIAQGOWDODFP7S4CA4T"
    aws_secret_access_key = "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"
    region_name = "us-east-1"

    dynamodb = boto3.client('dynamodb',
                            aws_access_key_id=aws_access_key,
                            aws_secret_access_key=aws_secret_access_key,
                            region_name=region_name)

    table_name = 'a3-imagelabels'

    response = dynamodb.scan(
        TableName=table_name,
        AttributesToGet=[
            'label',
            'image_path'
        ])
    all_items = []
    # print(response)
    for item in response['Items']:
        single_item = {'image_path': item['image_path'], 'label': item['label']}
        all_items.append(single_item)

    keys = all_items

    for key in keys:
        response = dynamodb.delete_item(
            TableName=table_name,
            Key=key)
        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            print("Error in deleting the item:", key, "\n Received response:", response['ResponseMetadata']['HTTPStatusCode'])
        else:
            print("Item deleted:", key)


def timenow():
    while True:
        print(str(int(datetime.now().timestamp() * 1000000)))


# timenow()


def deleteOS(key):
    OSurl = 'https://search-photo-gallery-bumzzdzztuk5upjw7g6cslniie.us-east-1.es.amazonaws.com/photo-gallery/_search?q=key:' + key
    esauth = ('Master', 'Master@123')
    headers = {"Content-Type": "application/json"}
    response = requests.get(OSurl, auth=esauth, headers=headers)
    res = response.json()
    print(res)
    docid = ''
    if 0 < len(res['hits']['hits']):
        docid = res['hits']['hits'][0]['_id']
        print(docid)

        OSurl = 'https://search-photo-gallery-bumzzdzztuk5upjw7g6cslniie.us-east-1.es.amazonaws.com/photo-gallery/_doc/' + str(docid)
        esauth = ('Master', 'Master@123')
        headers = {"Content-Type": "application/json"}
        response = requests.delete(OSurl, auth=esauth, headers=headers)
        res = response.json()
        print(res)
    else:
        print("Image",key,"not found")


delete_key = str(1649907579248783)
deleteOS(delete_key)

# test()
# scanned = scan()
# for item in scanned:
#     print(item)
# delete_all_items()

# put_items('cat', '1.jpg')
# put_items('cat', '2.jpg')
# put_items('dog', '4.jpg')
# put_items('cat', '2.jpg')
# put_items('cat', '3.jpg')
# put_items('cat', '4.jpg')
# put_items('dog', '1.jpg')
# put_items('nature', '2.jpg')
# put_items('nature', '3.jpg')
# put_items('mammal', '2.jpg')
# get_item('cat')

# cat = get_items('cat')
# print("cat:", cat)

# test = get_items('test')
# print("test:", test)

# dog = get_items('dog')
# print("dog:", dog)

# delete = delete_items('1.jpg')
# print("delete:", delete)
