from flask import Flask,Response,request,jsonify
import json
import pymongo
import urllib
from bson.objectid import ObjectId
import json_to_dict as jtd
import jwt
import datetime
from flask_bcrypt import Bcrypt
from functools import wraps
from flask_session import Session

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config['SECRET_KEY'] = 'f1a2c3e4r5e6c7o8g9n0i1t2i3o4n6'
SESSION_TYPE = 'redis'
app.config.from_object(__name__)
Session(app)


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


json_enc = "application/json"

#authorization decorator
def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        token = None
        #jwt is passed in the request header
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[1]
        print(token)
        if not token:
            return Response(
                response={
                    'success' : False,
                    'message' : 'Not authorized!'
                },
            status=403,
            mimetype=json_enc
            )
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            print(data)
        except Exception as ex:
            print(ex)
            return Response(
                response={
                    'success' : False,
                    'message' : 'Not authorized!'
                },
            status=403,
            mimetype=json_enc
            )
        return f(*args,**kwargs)
    return decorated



# authentication
@app.route('/login', methods=['POST'])
def login():
    auth = request.form
    resp = db.users.find_one({"email":auth['email']})
    resp = dict(resp)
    print(resp['password'])
    if not resp:
        return Response(
            response = json.dumps({
                "message":"email is not authorized!",
                }),
            status=403,
            mimetype=json_enc
        )
    # pswd = resp['password'].encode('utf-8')
    if bcrypt.check_password_hash(resp['password'],auth['password']):
        token = jwt.encode({'user': auth['email'], 
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            },
            app.config['SECRET_KEY'],
            algorithm='HS256')
        
        return Response(
            response = json.dumps({
                "token":token
                }),
            status=200,
            mimetype=json_enc
        )
    return Response(
        response = json.dumps(
            {
                "success": False,
                "message": "Incorrect Password!"
            }
        )
    )



@app.route('/signup',methods=["POST"])
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
                mimetype=json_enc
            )    
        user = {
            "first_name":request.form["first_name"],
            "last_name":request.form["last_name"],
            "roll_number":request.form["roll_number"],
            "department":request.form["department"],
            "year":request.form["year"],
            "email":request.form["email"],
            "password": bcrypt.generate_password_hash(request.form['password'].encode('utf-8'),10)
            }
        dbResponse = db.users.insert_one(user)
        return Response(
            response = json.dumps({
                "message":"user_created",
                "id":f"{dbResponse.inserted_id}"
                }),
            status=200,
            mimetype=json_enc
        )
    except Exception as ex:
        print(ex)
     

@app.route('/users/list',methods=["Get"])
@token_required
def get_some_users():
    print('herre')
    try:
        data = list(db.users.find())
        print(data[0]['_id'])
        resp = jtd.jsonify(data)
        
        return Response(
            response = json.dumps({
                "response": resp
                }),
            status=200,
            mimetype=json_enc
        )
    except Exception as ex:
        print(ex)
        return Response(
            response = json.dumps({
                "message":"cannot read users",
                }),
            status=500,
            mimetype=json_enc
        )

@app.route('/users/<string:id>/delete',methods=["Delete"])
@token_required
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
            mimetype=json_enc
        )
    except Exception as ex:
        print(ex)
        return Response(
            response = json.dumps({
                "success": False,
                "message": "something went wrong"
            }),
            status=500,
            mimetype=json_enc
        )

@app.route('/users/<string:id>', methods=["Get"])
@token_required
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
            mimetype=json_enc
        )
    except Exception as ex:
        print(ex)
        return Response(
            response = json.dumps({
                "success": False,
                "message": "Something went wrong!"
            }),
            status=500,
            mimetype=json_enc
        )

@app.route('/users/<string:id>/update', methods=["Put"])
@token_required
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
            mimetype=json_enc
        )
    except Exception as ex:
        print(ex)
        return Response(
            response = json.dumps({
                "success": False,
                "message": "Something went wrong!"
            }),
            status=500,
            mimetype=json_enc
        )

if __name__ == "__main__":
    app.run(port=5555,debug=True)