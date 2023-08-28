import json
import os
from flask import Blueprint, abort, render_template_string, session
from flask import Blueprint, flash, redirect, render_template, request
from models import Contacts, Post, getJson
 
from models import getJson,db
from werkzeug.utils import secure_filename

from utils import getRenderend, getfiles
from flask import current_app
admin = Blueprint('admin', __name__)

 
    
    
@admin.route("/uploader", methods=['GET', 'POST'])
def upload_file():
    params=current_app.config['params']
    admin_params=current_app.config['admin_params']
    if "user" in session and session['user'] ==admin_params['admin_user']:
       
        if request.method == 'POST':
            file = request.files['file']
            if (file is not None):
                filename = secure_filename(file.filename )
                app_path=current_app.root_path
                path=os.path.join(app_path,'static','assets','img',filename)
                print("path using os join: ",path)
       
                # path = os.path.join(".", path)
                try:
                    
                    file.save(path)
                    flash(f'successfully uploaded','success')
                except Exception as e:
                    
                    flash( f"error uploading: {str(e)}",'danger')
                
                    # Directory is writable, proceed with file upload
            else:
                flash(f'no file uploaded','warning')
            return redirect("/dashboard")
    else:
        return render_template("login.html", params=params)


@admin.route('/logout')
def logout():
    if('user' in session):
        session.pop('user')
    return redirect('dashboard')



@admin.route("/delete/<int:sno>", methods=['GET'])
def delete_post(sno):

    params=current_app.config['params']
    admin_params=current_app.config['admin_params']
    if "user" in session and session['user'] == admin_params['admin_user']:
        post = Post.query.filter(Post.sno == sno).first()
        if(post.sno==2):
            flash(f'you are not supposed to delete about page','danger')
            return redirect('/dashboard')
        db.session.delete(post)
        db.session.commit()
        return redirect("/dashboard")
    else:
        return render_template("login.html", params=params)


@admin.route("/edit/<int:sno>", methods=['GET', 'POST'])
def edit_post(sno):
    params=current_app.config['params']
    admin_params=current_app.config['admin_params']    
    if "user" in session and session['user'] == admin_params['admin_user']:
        if request.method == 'POST':
            box_title = request.form.get("title")
            sub_heading = request.form.get("sub")
            slug = request.form.get('slug')
            content = request.form.get('content')
            postby = request.form.get('postby')
            background_img = request.form.get('img')
            if ((box_title is not None) and (sub_heading is not None) and (slug is not None) and (content is not None) and (postby is not None) and (background_img is not None)):
                if (sno == 0 or sno is None):
                    entry = Post(title=box_title, sub_heading=sub_heading, slug=slug,
                                 content=content, postby=postby, background_img=background_img)
                    print("entry: ", entry)
                    db.session.add(entry)
                    db.session.commit()
                    flash(f'your post has been posted successfully having id {entry.sno}','success')
                    return redirect('/dashboard')
                else:
                    post = Post.query.filter(Post.sno == sno).first()
                    post.title = box_title
                    post.sub_heading = sub_heading
                    post.slug = slug
                    post.content = content
                    post.postby = postby
                    post.background_img = background_img
                    db.session.commit()
                    flash(f'your post has been updated successfully having id {post.sno}','success')
                    return redirect('/dashboard')
            else:
                flash(f'check the details your inserted','warning')
                return redirect('/dashboard')
        post = Post.query.filter(Post.sno == sno).first()
        return render_template("edit.html", params=params, posts=post, usercheck=True, sno=sno)
    else:
        flash(f'login before you do anything','danger')
        return render_template("login.html", params=params)
    
    
    
    
@admin.route("/image/<string:filename>", methods=['GET'])
def viewimage(filename):
    params=current_app.config['params']
    admin_params=current_app.config['admin_params']    
    if "user" in session and session['user'] == admin_params['admin_user']:
        if(filename):
            content=f"<h1>{filename}<h1>\n"
            image="{{url_for('static',filename='assets/img/"+filename+"')}}" 
            content+=f"<img src={image} /> \n"
            
         
            # Render the template with the custom environment and pass the variables
            rendered_body = getRenderend(content)
            return render_template_string(rendered_body)
        else:
            abort(403)
    else:
        return render_template("login.html", params=params)



@admin.route("/contact/delete/<int:sno>", methods=['GET'])
def deleteContact(sno):
    admin_params=current_app.config['admin_params']    
    if(sno is None or type(sno)!=int):
        abort(403)
    if "user" in session and session['user'] == admin_params['admin_user']:
        contacts = Contacts.query.filter(Contacts.sno==sno).first()
        db.session.delete(contacts)
        db.session.commit()
        flash(f'contact is succcesffully deleted','info')
        return redirect('/dashboard')
    else:
        return redirect('/dashboard')




@admin.route("/contact/view/<int:sno>", methods=['GET'])
def viewContact(sno):
    params=current_app.config['params']
    admin_params=current_app.config['admin_params']    
    if(sno is None or type(sno)!=int):
        abort(403)
    if "user" in session and session['user'] == admin_params['admin_user']:
        contacts = Contacts.query.filter(Contacts.sno==sno).first()
        content=f"<h1>name:   {contacts.name}</h1>\n"
        content+=f"<h2>email:   {contacts.email}</h2>\n"
        content+=f"<h2>phone:   {contacts.phone}</h2>\n"
        content+=f"<h2>message: </h2><p> {contacts.message}</p>\n"
     
        rendered_body = rendered_body = getRenderend(content)
        return render_template_string(rendered_body)
    else:
        return render_template("login.html", params=params)
    
    
    
@admin.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    # with current_app.app_context():
    params=current_app.config['params']
    admin_params=current_app.config['admin_params']    
    if "user" in session and session['user'] == admin_params['admin_user']:  
  
        path = os.path.join(admin.root_path+"/..","static/assets/img")
        files = getfiles(path)
        posts = Post.query.all()
        contacts = Contacts.query.all()
        return render_template("dashboard.html", params=params, posts=posts, usercheck=True, contacts=contacts, files=files)

    if request.method == "POST":
 
        username = request.form.get("email")
        userpass = request.form.get("pass") 
        if username == admin_params['admin_user'] and userpass == admin_params['admin_password']:
            # set the session variable
            
            session['user'] = username
            return redirect('/dashboard')
        flash('invalid attempt','danger')
        return redirect('/dashboard')
    else:
        return render_template("login.html", params=params)
