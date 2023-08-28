import json
import os
from flask import Blueprint, flash, redirect, render_template, request, url_for,current_app
from flask_login import current_user, login_required, login_user, logout_user
from models import User, db, getJson
 
from users.forms import LoginForm, RegistrationForm, ResetPasswordForm, ResetRequestForm, UpdateUserForm
from utils import decrypt, encrypt, getUUID, save_picture, sendMessage  
 
users = Blueprint('users', __name__)

 
 
 
    


def send_reset_email(user):

    mail_params=current_app.config['mail_params']
    secret_key=current_app.config['SECRET_KEY']
    token = user.get_reset_token(secret_key)
    subject='Password Reset Request'
    sender=mail_params["gmail-user"]
    recipients=[user.email]
    message = f'''To reset your password, visit the following link:
{url_for('users.reset_password', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    result=sendMessage(subject=subject,send_from=sender,send_to=recipients,body=message)
    return result

@users.route("/reset_request", methods=['GET', 'POST'])
def reset_request():

    params=current_app.config['params']
    
    if current_user.is_authenticated:
        return redirect("/home")
    form = ResetRequestForm()
    if form.validate_on_submit():
        user= User.query.filter(User.email==form.email.data).first()
        if(user is None):
            flash('Invalid Email','danger')
            return render_template('reset_request.html', params=params, form=form)
        result=send_reset_email(user)
        if(result):
            flash('email has been sucessfully sent to your email with instructions','success')
            return redirect('/login')
        flash('unable to send the reset email','warning') 
    return render_template('reset_request.html', params=params, form=form)



@users.route("/reset_password/<string:token>", methods=['GET', 'POST'])
def reset_password(token):
    params=current_app.config['params']
    secret_key=current_app.config['SECRET_KEY']
    if current_user.is_authenticated:
        return redirect("/home")
    result=User.verify_reset_token(token,secret_key)
    if(result is None):
        flash(f'token is invalid or expired','warning')
        return redirect('/reset_request')
    else:
        user=User.query.filter(User.id==result["user_id"]).first()
        print(user)
    form = ResetPasswordForm()
    if form.validate_on_submit():       
        hashed_password = encrypt(form.password.data)
        print("old password ",user.password)
        print("new hashed password ",user.password)
        user.password = hashed_password
        print(user)
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_password.html', params=params, form=form)



@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():

    params=current_app.config['params']
 
    forms=UpdateUserForm()
    if(forms.validate_on_submit()):
        profile=forms.profile.data
        if profile:
            path=os.path.join(current_app.root_path,'static','assets','img')
            filename=save_picture(profile,path)
            current_user.image_file=filename
        current_user.username=forms.username.data
        current_user.email=forms.email.data
        
        db.session.commit()
        flash(f'successfully updated your account','success')
        return redirect("/account")
    elif(request.method=='GET'):
        forms.username.data=current_user.username
        forms.email.data=   current_user.email
    return render_template('account.html',params=params,form=forms)



@users.route('/logoutuser')
def logoutuser():
    logout_user()
    flash(f'you are successfully logout','success')
    return redirect('home')


@users.route("/register", methods=['GET', 'POST'])
def register():

    params=current_app.config['params']
    
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():       
        encrypted_password=encrypt(form.password.data)
        user=User(password=encrypted_password,email=form.email.data,username=form.username.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}! you can login in', 'success')
        return redirect("/login")
    return render_template('register.html', params=params, form=form)





@users.route("/login", methods=['GET', 'POST'])
def login():

    params=current_app.config['params']
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user=User.query.filter(User.email==form.email.data).first()
        if(user is None):
            flash('Login Unsuccessful. Please check username and password', 'danger')
            return redirect('/login')
        check=decrypt(user.password,form.password.data)
        if check:
            flash('You have been logged in!', 'success')
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect('/home')
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('userlogin.html', params=params, form=form)
