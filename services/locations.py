from flask import Flask, jsonify
from flask.globals import request
import requests
import json
import os

app = Flask(__name__)

database_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

@app.route("/", methods=['GET'])
def init():
    ''' Application location service start '''
    return "Hello! Application of locations service." 

@app.route("/books", methods=['GET'])
def getBooks():
    ''' Return All Books list '''
    with open('{}/database/locations.json'.format(database_path), "r") as database:
        jsonDB = json.load(database)

    if 'books' in jsonDB:
        return jsonify(jsonDB['books'])

    return 'Error',404

@app.route("/books/<book_id>", methods=['GET'])
def getBook(book_id):
    ''' Get Book Data'''
    book_id = str(book_id)
    
    with open('{}/database/locations.json'.format(database_path), "r") as database:
        jsonDB = json.load(database)

    if 'books' in jsonDB:
        if book_id in jsonDB['books']:
            return jsonify(jsonDB['books'][book_id])

    return 'Error',404

@app.route("/books", methods=['POST'])
def createBook():
    ''' Create Book '''
    with open('{}/database/locations.json'.format(database_path), "r") as database:
        jsonDB = json.load(database)
    with open('{}/database/locations.json'.format(database_path), "w") as database:
        if 'books' not in jsonDB:
            jsonDB['books'] = {}
        if 'lastBookId' not in jsonDB:
            jsonDB['lastBookId'] = -1
        
        lastid = jsonDB['lastBookId']
        
        jsonDB['books'][lastid+1] = request.json
        jsonDB['books'][lastid+1]['id'] = lastid+1
        jsonDB['lastBookId'] = lastid+1
        json.dump(jsonDB,database,indent=4)

    return jsonify(jsonDB['books'][lastid+1])

@app.route("/books/<book_id>", methods=['PUT'])
def updateBook(book_id):
    ''' Update Book '''
    value = None

    with open('{}/database/locations.json'.format(database_path), "r") as database:
        jsonDB = json.load(database)
    with open('{}/database/locations.json'.format(database_path), "w") as database:
        if 'books' not in jsonDB:
            jsonDB['books'] = {}
        if 'lastBookId' not in jsonDB:
            jsonDB['lastBookId'] = -1
        
        if book_id in jsonDB['books']:
            value = {}
            book = request.json
            for(key,val) in book.items(): 
                jsonDB['books'][book_id][key] = val
    
            value = jsonDB['books'][book_id]
            json.dump(jsonDB,database,indent=4)

    if(value != None):
        return jsonify(value)
    return 'Error',404

@app.route("/books/<book_id>", methods=['DELETE'])
def deleteBook(book_id):
    ''' Delete Book '''
    book_id = str(book_id)
    value = None

    with open('{}/database/locations.json'.format(database_path), "r") as database:
        jsonDB = json.load(database)
    with open('{}/database/locations.json'.format(database_path), "w") as database:
        if 'books' not in jsonDB:
            jsonDB['books'] = {}
        if 'lastBookId' not in jsonDB:
            jsonDB['lastBookId'] = -1
        
        if book_id in jsonDB['books']:
            value={}
            value = jsonDB['books'][book_id]
            del jsonDB['books'][book_id]

        json.dump(jsonDB,database,indent=4)

    if(value != None):
        return jsonify(value)
    
    return 'Error',404

@app.route("/books/users/<user_id>", methods=['GET'])
def getUserBooks(user_id): 
    ''' Get User Books Id's '''
    user_id = str(user_id)
    
    with open('{}/database/locations.json'.format(database_path), "r") as database:
        jsonDB = json.load(database)

    if 'locations' in jsonDB:
        if user_id in jsonDB['locations']:
            return jsonify(jsonDB['locations'][user_id])

    return 'Error',404

@app.route("/books/take/<book_id>/<user_id>", methods=['POST'])
def takeBook(book_id,user_id):
    ''' User takes a specific book '''
    value = None
    book_id = str(book_id)
    user_id = str(user_id)

    try:
        user = requests.get("http://127.0.0.1:5000/users/{}".format(user_id))
    except requests.exceptions.ConnectionError:
        return "Service unvaliable"
    
    if not user:
        return 'Error',404

    with open('{}/database/locations.json'.format(database_path), "r") as database:
        jsonDB = json.load(database)
    with open('{}/database/locations.json'.format(database_path), "w") as database:
        if 'books' not in jsonDB:
            jsonDB['books'] = {}
        if 'lastBookId' not in jsonDB:
            jsonDB['lastBookId'] = -1
        
        if (book_id in jsonDB['books']):
            if user_id not in jsonDB['locations']:
                jsonDB['locations'][user_id] = []
            if "UsersLocations" not in jsonDB['books'][book_id]:
                jsonDB['books'][book_id]['UsersLocations'] = []

            jsonDB['books'][book_id]['UsersLocations'].append(user_id)
            jsonDB['locations'][user_id].append(book_id)

            value = jsonDB['books'][book_id]['UsersLocations']

        json.dump(jsonDB,database,indent=4)

    if(value != None):
        return jsonify(value)
    
    return 'Error',404

@app.route("/books/vacate/<book_id>/<user_id>", methods=['POST'])
def vacateBook(book_id,user_id):
    ''' User vacate a book '''
    value = None
    book_id = str(book_id)
    user_id = str(user_id)

    try:
        user = requests.get("http://127.0.0.1:5000/users/{}".format(user_id))
    except requests.exceptions.ConnectionError:
        return "Service unvaliable"
    
    if not user:
        return 'Error',404

    with open('{}/database/locations.json'.format(database_path), "r") as database:
        jsonDB = json.load(database)
    with open('{}/database/locations.json'.format(database_path), "w") as database:
        if 'books' not in jsonDB:
            jsonDB['books'] = {}
        if 'lastBookId' not in jsonDB:
            jsonDB['lastBookId'] = -1
        
        if (book_id in jsonDB['books']):

            if(("UsersLocations" in jsonDB['books'][book_id]) 
            and (user_id in jsonDB['locations'])
            and user_id in jsonDB['books'][book_id]['UsersLocations']):
                jsonDB['books'][book_id]['UsersLocations'].remove(user_id)
                jsonDB['locations'][user_id].remove(book_id)
                value = jsonDB['books'][book_id]['UsersLocations']

        json.dump(jsonDB,database,indent=4)

    if(value != None):
        return jsonify(value)
    
    return 'Error',404

if __name__ == '__main__':
    '''
    book = {
        "Name":"Scrum",
        "Authors":["Jeff Sutherland","J. J. Sutherland"],
        "Quantity": 10
    }
    book2 = {
        "Name":"Clean Code: A Handbook of Agile Software Craftsmanship",
        "Authors":["Robert C. Martin","Michael C. Feathers","Timothy R. Ottinger"],
        "Quantity": 5
    }
    '''
    app.run(port=5001,debug=True)