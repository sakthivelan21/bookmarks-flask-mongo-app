# === BookMarksController blueprint controller===
# Blueprint allow us to define the blueprint to the application
# which tells it has some routes for application and helps us to organize the code
from flask import Blueprint,request
from flask_mongo_app import db,token_required
from flask_pymongo import pymongo
from bson import ObjectId

#naming the Blueprint
bp = Blueprint('BookMarksController',__name__)

# getting the collection from database db
bookMarksCollection = pymongo.collection.Collection(db, 'BookMarks')

#CRUD Operation on collection bookmarks 

#getting all bookmarks 
@bp.route("/getAllBookMarks",methods=['GET'])
@token_required
def getAllBookMarks(userId):
    res={}
    try:
        # it will return pymongo.cursor.Cursor object
        bookMarks = bookMarksCollection.find({'userId':userId})
        print(bookMarks)
        bookMarks=list(bookMarks)
        status = {
                "statusCode":"200",
                "statusMessage":"BookMarks Data Retrieved Successfully from the Database."
            }
        #inorder to get the data and convert it into json 
        data= [{'id' : str(bookMark['_id']),'title':bookMark['title'],'text':bookMark['text'],'time':bookMark['time'],'isFavourite':bookMark['isFavourite']} for bookMark in bookMarks]   #list comprehension
        res['data']=data
    except Exception as e:
        print(e)
        status = {
                "statusCode":"400",
                "statusMessage":str(e)
            }
    res["status"] =status
    return res

# update the bookMark
@bp.route("/updateBookMark",methods=['PUT'])
@token_required
def updateBookMark(userId):
    res = {}
    try:
        req_body = request.json
        bookMarksCollection.update_one({"_id":ObjectId(req_body['id'])}, {"$set": req_body['updated_data']})
        print("BookMark Data Updated Successfully in the Database.")
        status = {
            "statusCode":"200",
            "statusMessage":"BookMark Updated Successfully in the Database."
        }
    except Exception as e:
        print(e)
        status = {
            "statusCode":"400",
            "statusMessage":str(e)
        }
    res["status"] =status
    return res
    
# delete the bookMark 
@bp.route("/deleteBookMark/<string:id>",methods=['DELETE'])
@token_required
def deleteBookMark(userId,id):
    res = {}
    try:
        bookMarksCollection.delete_one({"_id":ObjectId(id)})
        status = {
            "statusCode":"200",
            "statusMessage":"BookMark Deleted Successfully in the Database."
        }
        print(f"{id} bookmark removed successfully")
    except Exception as e:
        print(e)
        status = {
            "statusCode":"400",
            "statusMessage":str(e)
        }
    res["status"] =status
    return res

# insert the bookMark
@bp.route("/addBookMark",methods=['POST'])
@token_required
def addBookMark(userId):
    res = {}
    try:
        req_body = request.json
        req_body['userId']=userId
        bookMarksCollection.insert_one(req_body)            
        print("Book Mark Data Stored Successfully in the Database.")
        status = {
            "statusCode":"200",
            "statusMessage":"Book Mark Data Stored Successfully in the Database."
        }
    except Exception as e:
        print(e)
        status = {
            "statusCode":"400",
            "statusMessage":str(e)
        }
    res["status"] =status
    return res