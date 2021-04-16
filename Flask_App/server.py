from flask import Flask,Response,request,jsonify
import json
import pymongo
import urllib
from bson.objectid import ObjectId
import json_to_dict as jtd

app = Flask(__name__)
mongodb_uri="mongodb+srv://faceattend:" + urllib.parse.quote("stcet@123") + "@cluster0.af18n.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
try:
    client = pymongo.MongoClient(mongodb_uri)
    db = client.test
    # mongo.server_info()# trigger exception if cannot connect to db
except Exception as e:
    print(e)
    print("Error cannot connect to DB")
else:
    print("Connection to DB is successful")

@app.route('/users/add',methods=["POST"])
def create_user():
    try:
        resp = db.users.find({"email":request.form["email"]})
        resp = list(resp)
        if(resp):
            return Response(
                response = json.dumps({
                    "message":"email already exists",
                    }),
                status=403,
                mimetype="application/json"
            )    
        user = {
            "first_name":request.form["first_name"],
            "last_name":request.form["last_name"],
            "roll_number":request.form["roll_number"],
            "department":request.form["department"],
            "year":request.form["year"],
            "email":request.form["email"]
            }
        dbResponse = db.users.insert_one(user)
        # for attribute in dir(dbResponse):
        #     print(attribute)
        return Response(
            response = json.dumps({
                "message":"user_created",
                "id":f"{dbResponse.inserted_id}"
                }),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        print(ex)
     

@app.route('/users/list',methods=["Get"])
def get_some_users():
    try:
        data = list(db.users.find())
        print(data[0]['_id'])
        resp = jtd.jsonify(data)
        
        return Response(
            response = json.dumps({
                "response": resp
                }),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        print(ex)
        return Response(
            response = json.dumps({
                "message":"cannot read users",
                }),
            status=500,
            mimetype="application/json"
        )

@app.route('/users/<string:id>/delete',methods=["Delete"])
def delete_user(id):
    try:
        user = db.users.delete_one({"_id": ObjectId(id)})
        print("deleted")
        return Response(
            response = json.dumps({
                "success": True,
                "message": "User deleted"
            }),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        print(ex)
        return Response(
            response = json.dumps({
                "success": False,
                "message": "something went wrong"
            }),
            status=500,
            mimetype="application/json"
        )

@app.route('/users/<string:id>', methods=["Get"])
def get_one_user(id):
    try:
        user = db.users.find_one({"_id": ObjectId(id)})
        resp = jtd.jsonify_one(user)
        print("got it")
        return Response(
            response = json.dumps({
                "success": True,
                "response": resp
            }),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        print(ex)
        return Response(
            response = json.dumps({
                "success": False,
                "message": "Something went wrong!"
            }),
            status=500,
            mimetype="application/json"
        )

@app.route('/users/<string:id>/update', methods=["Put"])
def update_one_user(id):
    updates = {
            "first_name":request.form["first_name"],
            "last_name":request.form["last_name"],
            "roll_number":request.form["roll_number"],
            "department":request.form["department"],
            "year":request.form["year"],
            "email":request.form["email"]
            }
    try:
        user = db.users.find_one_and_update({"_id": ObjectId(id)},{"$set" : updates})
        resp = jtd.jsonify_one(user)
        print("got it")
        return Response(
            response = json.dumps({
                "success": True,
                "response": resp
            }),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        print(ex)
        return Response(
            response = json.dumps({
                "success": False,
                "message": "Something went wrong!"
            }),
            status=500,
            mimetype="application/json"
        )

if __name__ == "__main__":
    app.run(port=5555,debug=True)