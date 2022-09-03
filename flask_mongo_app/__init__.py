#importing Flask 
from flask import Flask,request,make_response,jsonify
import jwt
from flask_pymongo import pymongo
from flask_cors import CORS
import os 
from dotenv import load_dotenv
from functools import wraps


# loading the dotenv inorder to get the environment variables
load_dotenv()

con_string = os.getenv('MONGO_URL')

client = pymongo.MongoClient(con_string)

db = client.get_database('BookMarksAppDataBase')

# a function to create the flask app and utilize it from flask_mongo_app
def create_app():
    app = Flask(__name__)
    
    from flask_mongo_app import bookmarks,user
    # registering the blueprint of controllers with the flask application	
    app.register_blueprint(bookmarks.bp,url_prefix='/bookmarks')
    app.register_blueprint(user.bp,url_prefix='/user')
    CORS(app)
    return app 

# token authorization and verification
def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        token=None 
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
        if not token:
            return make_response(jsonify({'message':'Token is missing'}),401)
        try:
            data = jwt.decode(token,os.getenv('ACCESS_TOKEN_KEY'),algorithms="HS512")
        except jwt.ExpiredSignatureError:
            return make_response(jsonify({'message':'Token expired','status':'401'}))
        except Exception as e:
            print(e)
            return make_response(jsonify({'message':str(e),'status':'401'}))
        return f(data.get('userId'),*args, **kwargs)
    return decorated
