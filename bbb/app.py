from flask import Flask,request,render_template
from flask_pymongo import PyMongo
from pymongo import mongo_client
import pickle

login_user = None

app = Flask(__name__)
app.config["SECRET_KEY"] = "29c1a12e30114e28c0910e3a52acf3c052597301"
app.config["MONGO_URI"] = "mongodb+srv://lyproj1:lyproj1@cluster0.n8ty28s.mongodb.net/test?retryWrites=true&w=majority&ssl=true&tls=true&tlsAllowInvalidCertificates=true"

mongodb_client = PyMongo(app)
db = mongodb_client.db
print("---"*29,db)
@app.route('/')
def hello_world():
    return render_template("login.html")
# database={'nachi':'123','james':'aac','karthik':'asdsf'}

@app.route('/form_login',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        print(request)
        name1=request.form['username']
        pwd=request.form['password']
        login_user = db.users_db.find_one({'username': name1})

        if db.users_db.find_one({'username': name1}):
            if pwd == login_user['password']:
                # return render_template("home.html",name=name1)
                return {"status":"ok"}

    # return render_template("login.html",info='Invalid Password')
    return {"status":"not ok"}


if __name__ == '__main__':
    app.run()
