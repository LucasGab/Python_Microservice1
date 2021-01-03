from flask import Flask, jsonify
from flask.globals import request
import requests
import json
import os

app = Flask(__name__)

@app.route("/", methods=['GET'])
def init():
    ''' Application reports service start '''
    return "Hello! Application of reports service." 

@app.route("/reports/<user_id>", methods=['GET'])
def getReportUser(user_id):
    ''' Return All Books list '''
    user_id = str(user_id)
    value = None

    try:
        user = requests.get("http://127.0.0.1:5000/users/{}".format(user_id))
    except requests.exceptions.ConnectionError:
        return "Service unvaliable"

    if not user:
        return 'Error',404

    value = {}
    value['user'] = user.json()
    value['books'] = []

    try:
        books = requests.get("http://127.0.0.1:5001/books/users/{}".format(user_id))
    except requests.exceptions.ConnectionError:
        return "Service unvaliable"

    if not books:
        return 'Error',404 

    for bookId in books.json():
        try:
            book = requests.get("http://127.0.0.1:5001/books/{}".format(bookId))
        except requests.exceptions.ConnectionError:
            return "Service unvaliable"

        if book:
            value['books'].append(book.json())

    if(value != None):
        print(value)
        return jsonify(value)
    
    return 'Error',404

if __name__ == '__main__':
    app.run(port=5002,debug=True)