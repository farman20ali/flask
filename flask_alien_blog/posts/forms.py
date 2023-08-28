
from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from wtforms import StringField, TextAreaField,SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from models import Userposts

 
 

class PostForm(FlaskForm):
    # 'Username'  is the name of field
    # second argument is validators
    legend="Add Useful Info"
    title = StringField('Title', validators=[
        DataRequired(),Length(min=5)])
    sub_heading = StringField('Sub Heading', validators=[
        DataRequired(), Length(  min=5)])
 
    slug=StringField('Slug', validators=[
        DataRequired(),Length(min=5,max=30)])
    content=TextAreaField('Content', validators=[
        DataRequired(),Length(min=10)])
    background_img=StringField('Background image', validators=[
        DataRequired(),Length(min=2)])
    profile = FileField('Upload profile picture', validators=[
        FileAllowed(['jpg','png'])])
    submit = SubmitField('Post')
    def validate_slug(self,slug):
        post=Userposts.query.filter(Userposts.slug==slug.data).first()
        if(post):
            raise ValidationError('try different slug')

class UpdatePostForm(FlaskForm):
    # 'Username'  is the name of field
    # second argument is validators

    title = StringField('Title', validators=[
        DataRequired(),Length(min=5)])
    sub_heading = StringField('Sub Heading', validators=[
        DataRequired(), Length(  min=5)])
 
    slug=StringField('Slug', validators=[
        DataRequired(),Length(min=5,max=30)])
    content=TextAreaField('Content', validators=[
        DataRequired(),Length(min=10)])
    background_img=StringField('Background image', validators=[
        DataRequired(),Length(min=2)])
    profile = FileField('Upload profile picture', validators=[
        FileAllowed(['jpg','png'])])
    submit = SubmitField('Post')
 


 