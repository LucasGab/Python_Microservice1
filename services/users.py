from flask import Flask, jsonify
from flask.globals import request
import json
import os

app = Flask(__name__)

database_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

@app.route("/", methods=['GET'])
def init():
    ''' Application user service start '''
    return "Hello! Application of users service." 

@app.route("/users", methods=['GET'])
def getUsers():
    ''' Return All Users list '''
    with open('{}/database/users.json'.format(database_path), "r") as database:
        jsonDB = json.load(database)

    if 'users' in jsonDB:
        return jsonify(jsonDB['users'])
    
    return 'Error',404

@app.route("/users/<user_id>", methods=['GET'])
def getUser(user_id):
    ''' Get User Data'''
    user_id = str(user_id)

    with open('{}/database/users.json'.format(database_path), "r") as database:
        jsonDB = json.load(database)

    if 'users' in jsonDB:
        if user_id in jsonDB['users']:
            return jsonify(jsonDB['users'][user_id])

    return 'Error',404

@app.route("/users", methods=['POST'])
def createUser():
    ''' Create User '''
    with open('{}/database/users.json'.format(database_path), "r") as database:
        jsonDB = json.load(database)
    with open('{}/database/users.json'.format(database_path), "w") as database:
        if 'users' not in jsonDB:
            jsonDB['users'] = {}
        if 'lastUserId' not in jsonDB:
            jsonDB['lastUserId'] = -1
        
        lastid = jsonDB['lastUserId']
        
        jsonDB['users'][lastid+1] = request.json
        jsonDB['users'][lastid+1]['id'] = lastid+1
        jsonDB['lastUserId'] = lastid+1
        json.dump(jsonDB,database,indent=4)

    return jsonify(jsonDB['users'][lastid+1])

@app.route("/users/<user_id>", methods=['PUT'])
def updateUser(user_id):
    ''' Update User '''
    user_id = str(user_id)
    value = None

    with open('{}/database/users.json'.format(database_path), "r") as database:
        jsonDB = json.load(database)
    with open('{}/database/users.json'.format(database_path), "w") as database:
        if 'users' not in jsonDB:
            jsonDB['users'] = {}
        if 'lastUserId' not in jsonDB:
            jsonDB['lastUserId'] = -1
        
        if user_id in jsonDB['users']:
            value = {}
            user = request.json
            for(key,val) in user.items(): 
                jsonDB['users'][user_id][key] = val

            value = jsonDB['users'][user_id]
        
        json.dump(jsonDB,database,indent=4)

    if (value != None):
        return jsonify(value)

    return 'Error',404 

@app.route("/users/<user_id>", methods=['DELETE'])
def deleteUser(user_id):
    ''' Delete User '''
    user_id = str(user_id)
    value = None
    
    with open('{}/database/users.json'.format(database_path), "r") as database:
        jsonDB = json.load(database)
    with open('{}/database/users.json'.format(database_path), "w") as database:
        if 'users' not in jsonDB:
            jsonDB['users'] = {}
        if 'lastUserId' not in jsonDB:
            jsonDB['lastUserId'] = -1
        
        if user_id in jsonDB['users']:
            value={}
            value = jsonDB['users'][user_id]
            del jsonDB['users'][user_id]

        json.dump(jsonDB,database,indent=4)

    if(value != None):
        return jsonify(value)
    
    return 'Error',404

if __name__ == '__main__':
    '''
    user = {
        "FirstName": "James",
        "LastName": "Bond",
        "Email":"JamesBond@Email.com"
    }
    user2 = {
        "FirstName": "Warren",
        "LastName": "Buffett",
        "Email":"WarrenBuffett@Email.com"
    }
    '''
    app.run(port=5000,debug=True)