

import json
import math
from flask import Blueprint, flash, render_template, request,current_app
from models import Contacts, Post, getJson,db
from datetime import datetime
from utils import getRenderend, sendMessage


main = Blueprint('main', __name__)


 

@main.route("/contact", methods=['GET', 'POST'])
def contact():
 
    with current_app.app_context():
        params=current_app.config['params']
        mail_params=current_app.config['mail_params']
    if (request.method == 'POST'):
        # adding entry in database
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        if (len(name) > 0 and len(email) > 0 and len(phone) > 0 and len(message) > 0):
            entry = Contacts(name=name, phone=phone, message=message,
                             date=datetime.now(), email=email)
            db.session.add(entry)
            db.session.commit()
            
            result=sendMessage('New message from ' + name, mail_params["gmail-user"],
                        [mail_params['recipients']], message + "\n" + email+"\n" + phone)
            if(result):
                flash(f'message sent successfully', 'success')
            else:
                flash(f'error sending message', 'danger')
    return render_template('contact.html', params=params)




@main.route('/post/<string:post_slug>')
def getPost(post_slug):
    post = Post.query.filter_by(slug=post_slug).first()
    post.content = getRenderend(post.content)
    with current_app.app_context():
        params=current_app.config['params']
    return render_template('post.html', params=params, post=post)


@main.route('/about')
def getAbout():
    post = Post.query.filter_by(slug="about").first()
    post.content = getRenderend(post.content)
    with current_app.app_context():
        params=current_app.config['params']
    
    return render_template('about.html', params=params, post=post)


# @app.route('/', defaults={'total': 0})
# @app.route('/home', defaults={'total': 0})
# @app.route('/<int:total>')
# @app.route('/home/<int:total>')
def home(total):
    with current_app.app_context():
        params=current_app.config['params']
     
    count = db.session.query(Post).count()
    limit = params["home-page-posts"]
    if (total is None or total < limit):
        total = 0
    else:
        if (total % limit > 0):
            total = total-(total % limit)
        if (total > count):
            total = count-limit

    posts = Post.query.filter(Post.sno > count-total-limit).limit(limit
                                                                  ).all()
    totalposts=[]
    for post in posts:
        post.content = getRenderend(post.content)
        totalposts.append(post)
    reversed_posts = totalposts[::-1]

    return render_template('index.html',params=params, posts=reversed_posts, total=total, count=count, limit=limit)


@main.route('/home')
@main.route('/')

def index():
    with current_app.app_context():
        params=current_app.config['params']
       
    posts = Post.query.filter_by().all()
    count = len(posts)
    limit = params["home-page-posts"]
    page = request.args.get('page')
    last = math.floor(count/limit)

    if ((page is None) or (not str(page).isnumeric) or len(page) < 0):
        page = 1
    page = int(page)

    if (page == 1):
        prev = "#"
        next = "/?page="+str(page+1)
    elif (page > last):
        next = "#"
        prev = "/?page="+str(page-1)
    else:
        next = "/?page="+str(page+1)
        prev = "/?page="+str(page-1)

    total = (page-1)*limit
    reversed_posts = posts[::-1]
    posts = reversed_posts[total:(total+limit)]
    totalposts=[]
    for post in posts:
        post.content = getRenderend(post.content)
        totalposts.append(post)
    reversed_posts =totalposts
    return render_template('index.html', params=params, posts=reversed_posts, next=next, prev=prev)
