from flask import Blueprint, render_template, request, redirect, url_for, Response
from app import app, db, conn, cursor
from mod import Post, Picture, Tag, User_Likes, Comment
import os
from werkzeug.utils import secure_filename
from flask_login import current_user


posts = Blueprint('posts', __name__, template_folder='templates')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@posts.route('/')
def index():
    page = request.args.get('page')
    
    q = request.args.get('q')

    if q:
        post = Post.query.filter(Post.title.contains(q) | Post.body.contains(q))
    else:
        post = Post.query.order_by(Post.createDate.desc())


    if page and page.isdigit():
        page = int(page)
    else:
        page = 1
     
    pages = post.paginate(page=page, per_page=9)

    return render_template('posts/index.html', post=post, pages=pages)


@posts.route('/create', methods=['GET', 'POST'])
def create_post():
    tags = Tag.query.all()
    if request.method == 'POST':
        title = request.form.get('title')
        body = request.form.get('body')
        file = request.files['file']
        user = current_user
        for i in range(1):
            if request.form.getlist('tags')[i] == '2D':
                tag = Tag.query.filter(Tag.name == request.form.getlist('tags')[i]).first()
            if request.form.getlist('tags')[i] == '3D':
                tag = Tag.query.filter(Tag.name == request.form.getlist('tags')[i]).first() 


        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            pic = Picture(name = filename)
            db.session.add(pic)
            db.session.commit()
        
            try:
                post = Post(title=title, body=body, likes=0)
                post.pictures.append(pic)
                post.tags.append(tag)
                post.user.append(user)
                
                db.session.add(post)
                db.session.commit()
            except:
                return 'Something wrong!'
        return redirect(url_for('posts.index'))
    else:
        return render_template('posts/create_post.html', tags=tags)

@posts.route('/<slug>')
def post_detail(slug):
    post = Post.query.filter(Post.slug == slug).first_or_404()
    tags = post.tags
    
    return render_template('posts/post_detail.html', post=post, tags=tags)

@posts.route('/<slug>/add_like')
def add_like(slug):
    post = Post.query.filter(Post.slug == slug).first_or_404()
    user = current_user
    
    query = User_Likes.query.filter(User_Likes.post_id == post.id, User_Likes.user_id == user.id).first()
    if not query:
        post.likes += 1
        row=User_Likes(post_id=post.id, user_id=user.id)
        db.session.add(row)
    else:
        post.likes -= 1
        db.session.delete(query)
    db.session.commit()
    return Response(str(post.likes))

@posts.route('/<slug>/add_comment', methods=['GET', 'POST'])
def add_comment(slug):
    
    post = Post.query.filter(Post.slug == slug).first_or_404()
    user = current_user
    text_comment = request.args.getlist("text")
    current_comment = Comment(text=text_comment[0])
    current_comment.author.append(user)
    post.comment.append(current_comment)

    db.session.add(current_comment)

    db.session.commit()

    return Response(text_comment)

 

@posts.route('/tag/<slug>')
def tag_detail(slug):
    tag = Tag.query.filter(Tag.slug == slug).first_or_404()
    posts = tag.posts.all()
    return render_template('posts/tag_detail.html', tag=tag, posts=posts)

    