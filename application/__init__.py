from flask import Flask
from flask_pymongo import PyMongo
from pymongo import mongo_client
app = Flask(__name__)
app.config["SECRET_KEY"] = "29c1a12e30114e28c0910e3a52acf3c052597301"
app.config["MONGO_URI"] = "mongodb+srv://lyproj1:lyproj1@cluster0.n8ty28s.mongodb.net/test?retryWrites=true&w=majority&ssl=true&tls=true&tlsAllowInvalidCertificates=true"

# s = MongoClient("mongodb+srv://lyproj1:lyproj1@cluster0.n8ty28s.mongodb.net/test?retryWrites=true&w=majority&ssl=true", tlsCAFile=certifi.where())

#setup pymongo
mongodb_client = PyMongo(app)
db = mongodb_client.db
# client = mongo_client("mongodb+srv://lyproj1:lyproj1@cluster0.p5epipv.mongodb.net/?retryWrites=true&w=majority")
# db = client.test


from application import routes
