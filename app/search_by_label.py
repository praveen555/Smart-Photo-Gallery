
from flask import render_template

from app import webapp


@webapp.route('/search_by_label', methods=['GET'])
def search_label():
    return render_template('search_label.html')
