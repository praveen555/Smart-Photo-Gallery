import boto3
from flask import render_template, request
import requests
from app.connector import aws_url, bucket, aws_access_key_id, aws_secret_access_key, region_name
import base64
from app import folder, webapp

webapp.config['UPLOAD_FOLDER'] = folder


@webapp.route('/statistics_gallery', methods=['GET'])
def gallery_stats():
    return render_template('gallery_stats.html')