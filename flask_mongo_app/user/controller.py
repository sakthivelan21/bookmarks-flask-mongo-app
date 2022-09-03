# === UserController blueprint controller===
# Blueprint allow us to define the blueprint to the application
# which tells it has some routes for application and helps us to organize the code
from ast import Constant
from flask import Blueprint,request,make_response,jsonify
from flask_mongo_app import db,token_required
from flask_pymongo import pymongo
from bson import ObjectId
from datetime import datetime, timedelta
import os
import jwt
# for safely storing password and checking them
from werkzeug.security import generate_password_hash, check_password_hash

#naming the Blueprint
bp = Blueprint('UserController',__name__)

# getting the collection from database db
usersCollection = pymongo.collection.Collection(db, 'users')
tokenCollection = pymongo.collection.Collection(db,'token')


#CRUD Operation on collection user

#authenticate user
@bp.route("/authenticateUser",methods=['POST'])
def authenticateUser():
    res={}
    auth = request.json
    if not auth or not auth.get('username') or not auth.get('password'):
        return make_response(
            jsonify({"message": "Could not verify"}),
            401,
            {'WWW-Authenticate': 'Basic realm ="Login required"'}
        )
    try:
        # it will return pymongo.cursor.Cursor object
        user = usersCollection.find_one({'username':auth.get('username')})
        print(user)

        if not user:
            return {
                'status':{
                    'statusCode':'200',
                    'statusMessage':'username does not exists'
                }
            }
        if check_password_hash(user['password'], auth.get('password'))==False:
            return {
                'status':{
                    'statusCode':'200',
                    'statusMessage':'Invalid Password'
                }
            }
        status = {
                "statusCode":"200",
                "statusMessage":"Authenticated Successfully"
            }
        
        accessToken:Constant = jwt.encode({
            'userId': str(user['_id']),
            'exp': datetime.utcnow() + timedelta(minutes=10)
        }, os.getenv('ACCESS_TOKEN_KEY'),algorithm="HS512")
        
        refreshToken:Constant = jwt.encode({
            'userId':str(user['_id'])
        },os.getenv('REFRESH_TOKEN_KEY'),algorithm="HS512")

        tokenCollection.insert_one({'refreshToken':refreshToken,'userId':str(user['_id'])})
        
        #inorder to get the data and convert it into json 
        res['data']={'accessToken':accessToken,'refreshToken':refreshToken}

    except Exception as e:
        print(e)
        status = {
                "statusCode":"400",
                "statusMessage":str(e)
            }
    res["status"] =status
    return res

#removing refresh token while logout
@bp.route('/logout/<string:refreshToken>',methods=['DELETE'])
@token_required
def logout(userId,refreshToken):
    res = {}
    try:
        tokenCollection.delete_one({'refreshToken':refreshToken})
        status = {
            "statusCode":"200",
            "statusMessage":"User Refresh Toekn Deleted Successfully in the Database."
        }
        print(f"refresh Token removed successfully")
    except Exception as e:
        print(e)
        status = {
            "statusCode":"400",
            "statusMessage":str(e)
        }
    res["status"] =status
    return res

#refresh token every 10 minutes 
@bp.route("/refreshToken",methods=['POST'])
def refreshToken():
    res={}
    status={
            "statusCode":"200",
            "statusMessage":"token refreshed"
        }
    refreshToken:Constant = request.json.get('refreshToken')
    try:
        tokenData = tokenCollection.find_one({'refreshToken':refreshToken})
        if not tokenData:
            status={
                "statusCode":"400",
                "statusMessage":"token not found"
            }
        else:    
            accessToken:Constant = jwt.encode({
                'userId': str(tokenData['userId']),
                'exp': datetime.utcnow() + timedelta(minutes=10)
            }, os.getenv('ACCESS_TOKEN_KEY'),algorithm="HS512")
            res['data']={'accessToken':accessToken}
        
    except Exception as e:
        print(e)
        status = {
            "statusCode":"400",
            "statusMessage":str(e)
        }
    res["status"] =status
    return res
    

# adding new user
@bp.route('/addUser',methods=['POST'])
def addUser():
    res={}
    status={}
    data = request.json
    users = list(usersCollection.find({'username':data.get('username')}))
    print(users)
    if len(users)==0:
        try:
            data['password']=generate_password_hash(data.get('password'))
            usersCollection.insert_one(data)
            print("new user added Successfully in the Database.")
            status = {
                "statusCode":"200",
                "statusMessage":"new user created successfully"
            }
        except Exception as e:
            print(e)
            status = {
                "statusCode":"400",
                "statusMessage":str(e)
            }
    else:
        status = {
                "statusCode":"202",
                "statusMessage":"username already exists !!!"
            }

    res["status"] =status
    return res

# get user details
@bp.route("/getUserDetails",methods=['GET'])
@token_required
def getUserDetails(userId):
    res={}
    try:
        # it will return pymongo.cursor.Cursor object
        user = usersCollection.find_one({'_id':ObjectId(userId)})
        if not user:
            return {
                "status":{
                    "statusCode":"200",
                    "statusMessage":"user not exist"
                }
            }
        status = {
                "statusCode":"200",
                "statusMessage":"fetched user details"
            }
        res['data']={
            'mailId':user['mailId'],
            'name':user['name'],
            'username':user['username']
        }
    except Exception as e:
        print(e)
        status = {
                "statusCode":"400",
                "statusMessage":str(e)
            }
    res["status"] =status
    return res


# update user details 
@bp.route('/updateUserDetails',methods=['PUT'])
@token_required
def updateUserDetails(userId):
    res = {}
    try:
        req_body = request.json
        usersCollection.update_one({"_id":ObjectId(userId)}, {"$set": req_body})
        print("User Data Updated Successfully in the Database.")
        status = {
            "statusCode":"200",
            "statusMessage":"User Data Updated Successfully in the Database."
        }
    except Exception as e:
        print(e)
        status = {
            "statusCode":"400",
            "statusMessage":str(e)
        }
    res["status"] =status
    return res

# delete user 
@bp.route("/deleteUser",methods=['DELETE'])
@token_required
def deleteUser(userId):
    res = {}
    try:
        usersCollection.delete_one({"_id":ObjectId(userId)})
        status = {
            "statusCode":"200",
            "statusMessage":"user deleted Successfully in the Database."
        }
        print(f"{userId} user removed successfully")
    except Exception as e:
        print(e)
        status = {
            "statusCode":"400",
            "statusMessage":str(e)
        }
    res["status"] =status
    return res




    


