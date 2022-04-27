
from flask import render_template
from app import webapp


@webapp.route('/', methods=['GET', 'POST'])
@webapp.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index_page.html')
