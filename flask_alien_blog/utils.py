import uuid
from flask_mail import Mail 
import os
from flask import url_for
from jinja2 import Environment
import jwt
from datetime import datetime, timedelta
from flask_bcrypt import Bcrypt 
mail = Mail()

import secrets
from PIL import Image
from werkzeug.utils import secure_filename
bcrypt=Bcrypt() 
def getUUID():
    uuid_value = uuid.uuid4()
    string_uuid = str(uuid_value)
    return string_uuid

def encrypt(str):
    hashed_pw=bcrypt.generate_password_hash(str).decode('utf-8')  
    return hashed_pw
def decrypt(hash,str):
    result=bcrypt.check_password_hash(hash,str)
    return result

def dateFormat(datetime_obj, format):
    if (datetime_obj is None):
        datetime_obj = datetime.now()
    formated_date = datetime_obj.strftime(format)
    return formated_date


def getfiles(directory):

    list = os.listdir(directory)
    return list


def sendMessage(subject, send_from, send_to, body):
    try:
        mail.send_message(subject,
                          sender=send_from,
                          recipients=send_to,
                          body=body
                          )
        return True
    except Exception as e:
        print(e.with_traceback)
        return False



 
 

# Create a JWT token with a specific expiry time
def create_timed_token(payload,expiry_minutes,secret_key):
    expiry = datetime.utcnow() + timedelta(minutes=expiry_minutes)
    payload['exp'] = expiry
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token

# Decode and verify the JWT token
def decode_token(token,secret_key):
    try:
        payload = jwt.decode(token,secret_key, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        # Handle expired token
        return None
    except jwt.InvalidTokenError:
        # Handle invalid token
        return None

def save_picture(form_picture,root_path):
    picture_fn=rename_file(form_picture.filename)
    picture_path = os.path.join(root_path, picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

def rename_file(name):
    random_hex = secrets.token_hex(8)
    filename=secure_filename(name)
    _, f_ext = os.path.splitext(filename)
    picture_fn = random_hex + f_ext
    return picture_fn




def getRenderend(content):

    # safe_markup = Markup(post.content)
    # Create a custom Jinja environment
    custom_env = Environment()
    custom_env.globals['url_for'] = url_for

    # Render the template with the custom environment and pass the variables
    rendered_body = custom_env.from_string(content).render()

    # Format the datetime object as desired
    # date = dateFormat(post.date, "%d %B, %Y")
    # post = date
    return rendered_body