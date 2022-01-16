from flask import Flask
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config['SECRET_KEY'] = '75c623d0ba4e9f29babb765e'
app.config['SESSION_TYPE'] = 'filesystem'
bcrypt = Bcrypt(app)


from auction import routes
