
from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo,ValidationError
from users.routes import current_user
from models import User

class RegistrationForm(FlaskForm):
    # 'Username'  is the name of field
    # second argument is validators
    username = StringField('Username', validators=[
                           DataRequired(), Length(max=20, min=2)])
    email = StringField('Email', validators=[
        DataRequired(), Email()])
    password = PasswordField('Password', validators=[
        DataRequired(), Length(max=20, min=2)])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), Length(max=20, min=2), EqualTo('password')])
    submit = SubmitField('Sign Up')
    def validate_username(self,username):
        user=User.query.filter(User.username==username.data).first()
        if(user):
            raise ValidationError('username already exists choose different')
    def validate_email(self,email):
        user=User.query.filter(User.email==email.data).first()
        if(user):
            raise ValidationError('email already exists choose different')




class ResetRequestForm(FlaskForm):
    legend='Reset Password Form'
    email = StringField('Email', validators=[
        DataRequired(), Email()])
    submit = SubmitField('Send Request')
    def validate_email(self,email):
        user=User.query.filter(User.email==email.data).first()
        if(user is None):
            raise ValidationError('There is no such account with this email address. you must register first')

class ResetPasswordForm(FlaskForm):
    legend='Reset Password'
    password = PasswordField('Password', validators=[
        DataRequired(), Length(max=20, min=2)])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), Length(max=20, min=2), EqualTo('password')])
    submit = SubmitField('Reset Password')
    


class LoginForm(FlaskForm):
    # 'Username'  is the name of field
    # second argument is validators

    email = StringField('Email', validators=[
        DataRequired(), Email()])
    password = PasswordField('Password', validators=[
        DataRequired(), Length(max=20, min=2)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign In')


 
 

 
class UpdateUserForm(FlaskForm):
    # 'Username'  is the name of field
    # second argument is validators
    username = StringField('Username', validators=[
                           DataRequired(), Length(max=20, min=2)])
    email = StringField('Email', validators=[
        DataRequired(), Email()])
    profile = FileField('Upload profile picture', validators=[
        FileAllowed(['jpg','png'])])
    submit = SubmitField('Update')
    def validate_username(self,username):
        if username.data!=current_user.username:
            user=User.query.filter(User.username==username.data).first()
            if(user):
                raise ValidationError('username already exists choose different')
        
    def validate_email(self,email):
        if email.data!=current_user.email:
            user=User.query.filter(User.email==email.data).first()
            if(user):
                raise ValidationError('email already exists choose different')