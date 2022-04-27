
from flask import Flask

# EC2
folder = './static/images/'

# LOCAL
# folder = '/home/ubuntu/A2/app/static/images/'


webapp = Flask(__name__, static_url_path="", static_folder="static")
webapp.config['JSON_SORT_KEYS'] = False

from app import image_upload
from app import search_by_label
from app import clear_data
from app import gallery_stats
from app import show_images
from app import index