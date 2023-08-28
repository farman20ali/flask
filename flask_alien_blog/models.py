
import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import JSON
from utils import create_timed_token, decode_token
from flask_login import UserMixin,LoginManager
from flask_sqlalchemy import SQLAlchemy
db=SQLAlchemy()
login_manager=LoginManager() 
 
 
@login_manager.user_loader
def load_user(user_id):
    if(user_id and (user_id.isnumeric())):
        return User.query.get(int(user_id))

class Contacts(db.Model):
    __tablename__ = 'contacts'
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(12), nullable=False)
    message = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    email = db.Column(db.String(20), nullable=False)


class Json(db.Model):
    __tablename__ = 'json'
    sno = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50), nullable=False)
    data = db.Column(JSON)


class Post(db.Model):
    __tablename__ = 'post'
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    sub_heading = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime(timezone=True))
    postby = db.Column(db.String(80), nullable=False)
    slug = db.Column(db.String(80), nullable=False)
    background_img = db.Column(db.String(80), nullable=False)


class User(db.Model,UserMixin):
    __bind_key__ = 'site_db'
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Userposts', backref='author', lazy=True)
    def get_reset_token(self, secret_key,expires_min=2):
        payload={"user_id":self.id}
        token=create_timed_token(payload,expires_min,secret_key)
        return token
    @staticmethod
    def verify_reset_token(token,secret_key):
        return decode_token(token,secret_key)

    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.id}')"


class Userposts(db.Model):
    __bind_key__ = 'site_db'
    __tablename__ = 'post'
    sno = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    sub_heading = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False,
                     default=datetime.datetime.now())
    content = db.Column(db.Text, nullable=False)
    slug = db.Column(db.String(80), nullable=False)
    background_img = db.Column(db.String(80), nullable=False)
    postby = db.Column(db.String(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date}')"


def getContactsData():
    # execute a SELECT query using SQLAlchemy
    query = db.session.execute(db.select(Contacts).order_by(Contacts.name))

    # retrieve the results and convert them to a list of dictionaries
    results = query.scalars()
    data = [{'id': item.sno, 'name': item.name, 'email': item.email}
            for item in results]

    # do something with the data
    return data




def getJson(name):
    # execute a SELECT query using SQLAlchemy
    query = db.session.execute(db.select(Json).where(
        Json.filename == name).order_by(Json.filename))

    # retrieve the results and convert them to a list of dictionaries
    results = query.scalars()
    data = [{'sno': item.sno, 'filename': item.filename, 'data': item.data}
            for item in results]
    if (len(data) > 0):
        data = data[0]["data"]

    # do something with the data
    return data
