from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
app = Flask(__name__)
mysql = MySQLConnector(app,'full_friends')
@app.route('/')
def index():
    return redirect('/users')
@app.route('/users')
def users():
    query = 'select * from friend'
    friend = mysql.query_db(query)
    return render_template('index.html', all_friends=friend)
@app.route('/users/new')
def new():
    return render_template('new.html')
@app.route('/friends', methods=['POST'])
def create():
    query = "INSERT INTO friend (first_name, last_name, age, created_at, updated_at) VALUES (:first_name, :last_name, :age, NOW(), NOW())"
    data = {
             'first_name': request.form['first_name'],
             'last_name':  request.form['last_name'],
             'age': request.form['age']
           }
    mysql.query_db(query, data)
    return redirect('/users')
@app.route('/users/<friend_id>')
def friend(friend_id):
    query = 'SELECT * FROM friend WHERE id = :id'
    data = {
    'id': friend_id
    }
    friend = mysql.query_db(query, data)
    return render_template('info.html', all_friends=friend)
@app.route('/users/<friend_id>/edit')
def edit(friend_id):
    query = 'SELECT * FROM friend WHERE id = :id'
    data = {
    'id': friend_id
    }
    friend = mysql.query_db(query, data)
    return render_template('edit.html', all_friends=friend)
@app.route('/process/<friend_id>', methods=['POST'])
def process(friend_id):
    query = 'UPDATE friend SET first_name = :first_name, last_name = :last_name, age = :age, updated_at = NOW() WHERE id = :id'
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'age': request.form['age'],
        'id': friend_id
        }
    mysql.query_db(query, data)
    return redirect('/users/'+str(friend_id))
@app.route('/destroy/<friend_id>')
def destroy(friend_id):
    query = 'DELETE FROM friend WHERE id = :id'
    data = {
        'id': friend_id
        }
    mysql.query_db(query, data)
    return redirect('/users')
app.run(debug=True)
