from flask import Flask,Response,request
import json
import pymongo

app = Flask(__name__)

try:
    mongo = pymongo.MongoClient(
        host="localhost",
        port=27017,
        serverSelectionTimeoutMS=10
        )
    db = mongo.company
    mongo.server_info()# trigger exception if cannot connect to db
except:
    print("Error cannot connect to DB")
else:
    print("Connection to DB is successful")

@app.route('/users',methods=["POST"])
def create_user():
    try:
        user = {
            "name":request.form["name"],
            "lastname":request.form["lastname"]
            }
        dbResponse = db.users.insert_one(user)
        print(dbResponse.inserted_id)
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
     

@app.route('/users',methods=["Get"])
def get_some_users():
    try:
        data = list(db.users.find())
        print(data[0]['_id'])
        resp = []
        for i in data:
            obj = {}
            for j in i.keys():
                obj[j] = str(i[j])
            resp.append(obj)
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

if __name__ == "__main__":
    app.run(port=5555,debug=True)