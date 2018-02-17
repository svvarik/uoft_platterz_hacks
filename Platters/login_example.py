from flask import Flask, render_template, url_for, request, session, redirect
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'userlogin'
app.config['MONGO_URI'] = 'mongodb://platters_hacks:platters@ds227168.mlab.com:27168/platters_hacks'
MONGODB_URI = 'mongodb://platters_hacks:platters@ds227168.mlab.com:27168/platters_hacks'
client = MongoClient(MONGODB_URI)
db = client.get_database('platters_hacks')

@app.route('/')
def index():
    if 'username' in session:
        return 'You are logged in as ' + session['username']
    return render_template('index.html')

@app.route('/home', methods=['POST'])
def login():
    users = db.users
    login_user = users.find_one({'name' : request.form['username']})
    if login_user:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
            session['username'] = request.form['username']
            #return redirect(url_for('home/<name?'))
            return "log in"
    return 'Invalid username/password combination'


@app.route('/register', methods=['POST', 'GET'])
#@app.route('/user_info', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = db.users
        existing_user = users.find_one({'name' : request.form['username']})
        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'name' : request.form['username'], 'password' : hashpass})
            session['username'] = request.form['username']
            return render_template("user_info.html")
        return 'That username already exists!'
    return render_template("register.html")


if __name__ == '__main__':
    app.secret_key = 'kettle'
    app.run(debug=True)