from datetime import datetime

import boto3
import requests
from flask import render_template, request
from app.connector import aws_url, bucket, aws_access_key_id, aws_secret_access_key, region_name
from app import webapp

folder = './static/images/'

extensions = ['png', 'jpg', 'jpeg']


# @webapp.route('/', methods=['GET', 'POST'])
# @webapp.route('/index_page', methods=['GET', 'POST'])
# def index_page():
#     return render_template('index_page.html')


@webapp.route('/image_upload', methods=['POST', 'GET'])
def image_upload():
    return render_template('image_upload.html', msg=0)


@webapp.route('/display_image', methods=['POST', 'GET'])
def display_image():
    if request.method == 'POST':
        # Last value of image
        key_id = str(int(datetime.now().timestamp() * 1000000))
        image = request.files['img_file']

        # get the extension name of the file and convert it in lowercase
        filename = image.filename
        filename_list = filename.split(".")
        typeimg = filename_list[len(filename_list) - 1]

        imagename = str(key_id) + '.' + str(typeimg)
        url = "https://mhjwruzkb4.execute-api.us-east-1.amazonaws.com/v1/upload/a2-13032022/" + str(imagename)
        headers = {"Content-Type": "image/" + typeimg}

        # print("url:", url)
        # print("headers:", headers)
        response = requests.put(url, data=image, headers=headers)

        print(response)

        if typeimg in extensions:  # First check if a valid file is present

            # Saving file to local storage (needed because it would not save to S3 directly from Form POST data)
            # new_name = os.path.join(folder, str(key_id) + '.' + str(typeimg))
            # image.save(new_name)
            imagepath = "images/" + imagename
            s3_image = aws_url + imagepath
            print(s3_image)
            # Save to S3
            # s3 = boto3.client('s3',
            #                   aws_access_key_id=aws_access_key_id,
            #                   aws_secret_access_key=aws_secret_access_key,
            #                   region_name=region_name)
            # s3.upload_file(new_name, bucket, imagename,
            #                ExtraArgs={"ContentType": image.content_type}
            #                )
            # Removing file from local storage
            # os.remove(new_name)

            # Call the AWS Rekogition Service here
            metadata_label, metadata_confidence = [], []
            client = boto3.client('rekognition',
                                  aws_access_key_id=aws_access_key_id,
                                  aws_secret_access_key=aws_secret_access_key,
                                  region_name=region_name)
            response = client.detect_labels(Image={'S3Object': {'Bucket': bucket, 'Name': imagepath}}, MaxLabels=7)

            print('Detected labels for ' + s3_image)
            print()
            for label in response['Labels']:
                # print("Label: " + label['Name'])
                # print("Confidence: " + str(label['Confidence']))

                # Store in lists to display at front end also
                metadata_label.append(label['Name'])
                metadata_confidence.append(format(label['Confidence'], '.2f'))

            data = zip(metadata_label, metadata_confidence)

            return render_template("display_image.html", user_image=s3_image, x=key_id, msg=3, data=data)

        else:
            # return to the main page with a message to add the correct file type.
            return render_template("image_upload.html", msg=-1)
