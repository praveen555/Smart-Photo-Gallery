
from flask import jsonify

from app import webapp
from werkzeug import exceptions


@webapp.errorhandler(exceptions.HTTPException)
def my_error_processor(e):
    print("Exception caught!")
    print(str(e.code) + " " + e.name)
    dictError = {
        "success": "false",
        "error": {
            "code": e.code,
            # "error": e.name,
            "message": e.description
        }
    }
    return jsonify(dictError)


