from app import db
from . import main

from flask import (
	Flask, 
	render_template, 
	url_for, 
	request, 
	redirect, 
	request,
	flash, 
	make_response,
	session,
	current_app
)

from flask_login import (
	LoginManager, 
	UserMixin,
	login_required,
	login_user, 
	logout_user,
	current_user
)

from .forms import ContactForm, LoginForm
from app.models import User

"""
Доступ к куки
Для доступа к куки используется атрибут cookie объекта request. 
cookie — это атрибут типа словарь, содержащий все куки, отправленные браузером.
"""
@main.route('/cookie/')
def cookie():
	if not request.cookies.get('foo'):
		res = make_response("Setting a cookie")
		res.set_cookie('foo', 'bar', max_age=60*60*24*365*2)
	else:
		res = make_response("Value of cookie foo is {}".format(request.cookies.get('foo')))
		return res


@main.route('/logout/', methods=['post', 'get'])
@login_required
def logout():
	logout_user()
	flash("You have been logged out.")
	return redirect(url_for('login'))


@main.route('/admin/')
@login_required
def admin():
    return render_template('admin.html')


@main.route('/login/', methods=['post', 'get'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('admin'))
	form = LoginForm()
	if form.validate_on_submit():
		user = db.session.query(User).filter(User.username == form.username.data).first()
		if user and user.check_password(form.password.data):
			login_user(user, remember=form.remember.data)
			return redirect(url_for('admin'))

		flash("Invalid username/password", 'error')
		return redirect(url_for('login'))
	return render_template('login.html', form=form)


@main.route('/')
def index():
	return render_template('index.html')


if __name__ == '__main__':
	manager.run()