from application import app
from flask import render_template, request, redirect, flash, url_for, session, jsonify
import json
from bson import ObjectId
from .forms import *
from application import db
from datetime import datetime
import jwt, datetime
from functools import wraps
# login_user = None

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token=None
        if 'x-access-token' in request.headers:
            token=request.headers['x-access-token']

        if not token:
            return jsonify({'message':"missing token"}), 401
        try:
            data=jwt.decode(token, app.config['SECRET_KEY'],algorithms=['HS256'])
            current_user=data['user'] #db.users_db.find_one({'username': data['user']})['username']
        except:
            return jsonify({'message':'Invalid Token'}), 401

        return f(current_user, *args, **kwargs)
    return decorated

@app.route('/login', methods=['POST',  'GET'])
def login():
    # global login_user
    if request.method == 'POST':
        form = loginform(request.form)
        print(form.uname.data,form.passwd.data)
        username = form.uname.data
        passwd = form.passwd.data
        login_user = db.users_db.find_one({'username': username})

        if db.users_db.find_one({'username': username}):
            if passwd == login_user['password']:
                token=jwt.encode({"user":username, "exp":datetime.datetime.utcnow()+datetime.timedelta(minutes=40)}, app.config['SECRET_KEY'])
                return jsonify({'token':token})

        return 'Invalid username/password combination'
    else:
        form = loginform()
    return 'ok'

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        form = registerform(request.form)
        username = form.uname.data
        passwd = form.passwd.data
        emaill = form.email.data

        if db.users_db.find_one({'username': username}):
            return ('That username already exists!')
        else:
            db.users_db.insert_one({
                "username" : username,
                "password" : passwd,
                "email" : emaill
            })
            flash("User sucessfully registered", "success")
            return redirect("/login")

    else:
        form = registerform()

    return render_template("register.html", form = form)
        #     session['username'] = request.form['username']
        #     # hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
        #     users.insert_one({'name' : request.form['username'], 'password' : request.form['pass']})
        #     return redirect(url_for('index'))
        
        # return 'That username already exists!'

    # return render_template('register.html')


@app.route("/add_todo", methods = ['POST', 'GET'])
def add_todo():
    # global login_user
    # print(login_user)
    if login_user:
        if request.method == "POST":
            form = TodoForm(request.form)
            todo_name = form.name.data
            todo_description = form.description.data
            completed = form.completed.data

            db.todo_flask.insert_one({
                "username" : login_user["username"],
                "name": todo_name,
                "description": todo_description,
                "completed": completed,
                "date_created": datetime.utcnow()
            })
            flash("Todo successfully added", "success")
            return redirect("/add_todo")
        else:
            form = TodoForm()
        return render_template("add_todo.html", form = form) 
    else:
        # form = loginform()
        flash("Please log-in to continue")
        return redirect("/login")


@app.route("/add_plant", methods = ['POST', 'GET'])
def add_plant():
        if request.method == "POST":
            form = plantform(request.form)
            plant_name = form.name.data
            plant_sci = form.Sciname.data
            plant_description = form.description.data
            plant_ins = form.plantinginstruction.data
            plant_img = form.img.data
            plant_spl = form.caretips.data
            

            db.plants_db.insert_one({
                "name": plant_name,
                "Sciname" : plant_sci,
                "description": plant_description,
                "instruction": plant_ins,
                "care tips" : plant_spl,
                "img" : plant_img
            })
            flash("Plant successfully added", "success")
            return redirect("/add_plant")
        else:
            form = plantform()
        return render_template("add_plant.html", form = form) 


@app.route("/all_plants")
def get_plants():
        plants = []
        for p in db.plants_db.find():
            # print("-->",todo)
            plants.append(p)
        print(p)
        return render_template("view_plants.html", plants = plants)


@app.route("/user_todos")
@token_required
def get_todos(current_user):
    # global login_user
    # print(login_user)
    # if login_user:
    todos = []
    print(current_user)
    for todo in db.tasks.find({'username': current_user}):
        todo["_id"]=str(todo["_id"])
        todos.append(todo)
    print(todos)
    return jsonify({"tasks":todos})

@app.route("/delete_todo/<id>")
def delete_todo(id):
    db.todo_flask.find_one_and_delete({"_id": ObjectId(id)})
    flash("Todo successfully deleted", "success")
    return redirect("/")


@app.route("/update_todo/<id>", methods = ['POST', 'GET'])
def update_todo(id):
    if request.method == "POST":
        form = TodoForm(request.form)
        todo_name = form.name.data
        todo_description = form.description.data
        completed = form.completed.data

        db.todo_flask.find_one_and_update({"_id": ObjectId(id)}, {"$set": {
            "name": todo_name,
            "description": todo_description,
            "completed": completed,
            "date_created": datetime.utcnow()
        }})
        flash("Todo successfully updated", "success")
        return redirect("/")
    else:
        form = TodoForm()

        todo = db.todo_flask.find_one_or_404({"_id": ObjectId(id)})
        print(todo)
        form.name.data = todo.get("name", None)
        form.description.data = todo.get("description", None)
        form.completed.data = todo.get("completd", None)

    return render_template("add_todo.html", form = form)

#question
@app.route("/add_question", methods = ['POST', 'GET'])
@token_required
def add_ques(current_user):
    # global login_user
    # print(login_user)
    # if login_user:
    if request.method == "POST":
        form = queform(request.form)
        question = form.question.data
        q_image = form.image.data

        db.forum.insert_one({
            "user": current_user,
            "title" : question,
            "image": q_image,
            "likes": 0,
            "comments":[]
        })
        flash("Comment successfully added", "success")
        return 'ok'
    else:
        form = queform()
    return render_template("add_todo.html", form = form) #---------------ye apne react ke hissab se change
    # else:
    #     # form = loginform()
    #     flash("Please log-in to continue")
    #     return redirect("/login")

#comment
@app.route("/add_comment")
def add_comment():
        if login_user:
            if request.method == "POST":
                form = replyform(request.form)
                cmt_question = form.question.data
                cmt_reply = form.answer.data

                for todo in db.forum.find({'question': cmt_question}):
                    todo["comments"].append({"user":login_user["username"], "comment":cmt_reply})
            else:
                form = queform()
                return render_template("add_todo.html", form = form)


@app.route("/delete_question/<id>")
def delete_q(id):
    db.forum.find_one_and_delete({"_id": ObjectId(id)})
    flash("Question successfully deleted", "success")
    return redirect("/")

@app.route("/likequestion")
def like_question(question):
    if login_user:
        for todo in db.forum.find({'question': question}):
            todo["likes"]+=1

@app.route("/all_discussions")
def get_diss():
        diss = []
        for p in db.forum.find():
                p["_id"]=str(p["_id"])
                diss.append(p)
        print(diss)
        return jsonify({"questions":diss})

@app.route("/discussions/<id>")
def search_question(id):
    t = db.forum.find({"_id": ObjectId(id)})[0]
    print(t)
    t["_id"]=str(t["_id"])
    # lst=[]
    # for t in db.forum.find({"_id": ObjectId(id)}):
    #      t["_id"]=str(t["_id"])
        #  lst.append(t)
    return jsonify({"question":t})