from flask import Flask, jsonify
from .db import Session

app = Flask(__name__)

from todo_app import routes


@app.teardown_appcontext
def cleanup(resp_or_exc):
    Session.remove()


@app.errorhandler(404)
def page_not_found(e):
    msg = str(e)
    response = {'message': msg, 'status': 'Failure'}
    return jsonify(response), 404
