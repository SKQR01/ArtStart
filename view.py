from app import app, login_manager, db
from flask import render_template, redirect, url_for, request
from flask_login import login_user, logout_user, login_required, current_user
from mod import User, Picture
from werkzeug.utils import secure_filename
import os

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

@app.route('/')
def index():
	return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		form_user = request.form.get('login')
		user = User.query.filter(User.nickname==form_user).first()
		login_user(user)
		return redirect(url_for('index'))
	else:
		return render_template('users/login.html')
	
@app.route('/register', methods=['GET', 'POST'])
def reg_user():
	if request.method == 'POST':
		nickname = request.form.get('nickname')
		email = request.form.get('email')
		password = request.form.get('password')
		confirm_password = request.form.get('confirm_password')
		
		if confirm_password == password:
			u = User(nickname=nickname, email=email, password=password, active=True)
			db.session.add(u)
			db.session.commit()
			return redirect(url_for('index'))

	return render_template('users/user_register.html')

	
@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('posts.index'))


@app.route('/home')
@login_required
def home():
	u = current_user
	avatar = u.avatar
	return render_template('users/user_profile_home.html', user_profile = u, avatar = avatar)

@app.route('/home/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
	if request.method == 'POST':
		file = request.files['avatar']
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'] + r'\avatars', filename))

			pic = Picture(name = filename)
			db.session.add(pic)
			
			if current_user.avatar:
				for i in current_user.avatar:
					path = os.path.join(app.config['UPLOAD_FOLDER'] + r'\avatars\\'[:-1], i.name)
					os.remove(path)
			try:
				current_user.avatar.clear()
				
				current_user.avatar.append(pic)
				db.session.commit()
							
				return redirect('/home')
			except:
				return 'Something wrong!'
	else:
		return render_template('users/user_profile_edit.html')