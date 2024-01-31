from flask_app import app
from flask import Flask, render_template, request, redirect, session
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.models_user import Users

@app.route('/')
def index():
    users = Users.get_all()
    return render_template('index.html', users = users)

@app.route("/into", methods= ["POST"])
def create():
    # call the get all classmethod to get all friends
    if Users.validate_user(request.form):
        Users.create(request.form)
        # redirect to the route where the burger form is rendered.
        return redirect('/')
    else:
        
        
        print('fail')
        return redirect("/switch")

@app.route('/switch')
def switch():
    return render_template('create.html')

@app.route('/home')
def home():
    return redirect('/')

@app.route('/show/<int:user_id>')
def show(user_id):
    data = {
        'id' : user_id
    }
    user = Users.get_one(data)
    return render_template('display.html', user = user)

@app.route('/get/<int:user_id>')
def get(user_id):
    data = {
        'id' : user_id
    }
    user = Users.get_one(data)
    return render_template('edit.html', user = user)

@app.route("/update/<int:user_id>", methods =['POST'] )
def update(user_id):
    Users.update(request.form, user_id)
    return redirect('/')

@app.route("/delete/<int:user_id>")
def delete(user_id):
    data = {
        'id' : user_id
    }
    Users.delete(data, user_id)
    return redirect('/')

