import json
from flask import Blueprint, abort, current_app, flash, redirect, render_template, request
from flask_login import current_user, login_required
from models import User, Userposts, getJson,db
from posts.forms import PostForm, UpdatePostForm
from utils import getRenderend 
 

posts = Blueprint('posts', __name__)

 
 
    
@posts.route('/userpost/new', methods=['GET', 'POST'])
@login_required
def new_post():
    forms=PostForm()
    with current_app.app_context():
        params=current_app.config['params']
 
    if forms.validate_on_submit():
 
        post=Userposts(user_id=current_user.id,title=forms.title.data,sub_heading=forms.sub_heading.data,content=forms.content.data,slug=forms.slug.data,background_img=forms.background_img.data,postby=current_user.username)
    
        db.session.add(post)
        db.session.commit()
        flash('you successfully created the post','success')
        return redirect('/account')
    return render_template('create_post.html',params=params,form=forms )




@posts.route('/userpost/<int:sno>', methods=['GET'])
def user_post(sno):
    with current_app.app_context():
        params=current_app.config['params']
    if(not sno or type(sno)!=int):
        flash(f'no url path')
        return redirect('/home')
    post = Userposts.query.filter(Userposts.sno==sno).first()
    if(not post):
        abort(403)
    post.content = getRenderend(post.content)
    return render_template('post.html', params=params, post=post)

@posts.route('/userpost')
def all_user_post():
    with current_app.app_context():
        params=current_app.config['params']
 
    pg = request.args.get('page', 1, type=int)
    post =Userposts.query.order_by(Userposts.date.desc()).paginate(per_page=5,page=pg)
    return render_template('user_post.html', params=params ,posts=post)


@posts.route('/userpost/<int:sno>/update', methods=['GET', 'POST'])
@login_required
def update_post(sno):
    with current_app.app_context():
        params=current_app.config['params']
 
    form=UpdatePostForm()
    if(not sno or type(sno)!=int):
        abort(403)
    post = Userposts.query.get_or_404(sno)
    if post.author != current_user:
        abort(403)
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.backgrount_img= form.background_img.data
        post.sub_heading=form.sub_heading.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect('/userpost/'+str(post.sno))
    elif request.method == 'GET':
        form.title.data = post.title
        form.sub_heading.data = post.sub_heading
        form.content.data = post.content
        form.slug.data = post.slug
        form.background_img.data=post.background_img
    legend="Update Post"
    return render_template('create_post.html', params=params, form=form,legend=legend)




@posts.route('/userpost/<int:sno>/delete', methods=['GET','DELETE','POST'])
@login_required
def delete_userpost(sno):
    if(not sno or type(sno)!=int):
        abort(403)
    post = Userposts.query.get_or_404(sno)
    if post is None:
        abort(403)
    if post.author != current_user:
        abort(403)
    if request.method=='POST':
        db.session.delete(post)
        db.session.commit()
        flash(f'successfully deleted')
        return redirect("/userpost")
    flash(f'invalid request')
    return redirect("/userpost")


@posts.route('/userpost/<string:username>')
def  specific_user_post(username):
    with current_app.app_context():
        params=current_app.config['params']
    pg = request.args.get('page', 1, type=int)
    user=User.query.filter_by(username=username).first_or_404()
    post =Userposts.query.order_by(Userposts.date.desc()).filter(Userposts.author==user).paginate(per_page=5,page=pg)
    return render_template('user_post.html', params=params ,posts=post,user=user)

