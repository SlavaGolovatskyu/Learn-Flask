import auxiliary_functions
from validation.check_len import *
from datetime import datetime

from flask import (
    Flask, 
    render_template, 
    url_for, 
    request, 
    redirect
)

from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Article(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String(100), nullable = False)
	# nullable - если не будет данных оно не позволит создать текст.
	# db.String() всередине скобок можно указать максимальную длинну текста.
	intro = db.Column(db.String(300), nullable = False)
	text = db.Column(db.Text, nullable = False)
	date = db.Column(db.DateTime, default = datetime.utcnow)

	def __repr__(self):
		return '<Article %r>' % self.id


class Account(db.Model):
	user_id = db.Column(db.Integer, primary_key = True)
	email = db.Column(db.String(50), nullable = False)
	password = db.Column(db.String(100), nullable = False)
	date_reg = db.Column(db.DateTime, default = datetime.utcnow)

	def __repr__(self):
		return '<Account %r>' % self.user_id


@app.route('/')
def home_page():
	return render_template('index.html')

@app.route('/user/<int:id>')
def success_sign_in(id):
	account = Account.query.get(id)
	return render_template('user_account.html', account=account)


@app.route('/sign-in', methods=['POST', 'GET'])
def sign_in():
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		account = Account.query.filter_by(email=email).first()	
		try:
			if account.password == password:
				return redirect(url_for(f'/user/{account.user_id}', is_sign = True))
		except:
			return 'ghg'
		return password_is_not_valid()
	else:
		return render_template('sign_in.html')


@app.route('/sign-up', methods=['POST', 'GET'])
def sign_up():
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		account = Account(email=email, password=password)
		is_validation = check_len_all_data(email, password)
		try:
			Checking_for_the_existence_of_an_account = Account.query.filter_by(email=email).first()
			if Checking_for_the_existence_of_an_account.password == password:
				return An_account_with_the_same_name_already_exists()
		except:		
			try:
				if is_validation[0] and is_validation[1]:
					db.session.add(account)
					db.session.commit()
					account_info = Account.query.filter_by(email=email).first()
					return redirect(f'/user/{account_info.user_id}')
				return return_error_message(is_validation[0], is_validation[1])
			except:
				return account_has_not_been_created()
	else:
		return render_template('sign_up.html')


@app.route('/posts')
def posts():
	articles = Article.query.order_by(Article.date.desc()).all()
	return render_template('posts.html', articles=articles)


@app.route('/posts/<int:id>')
def post_detail(id):
	article = Article.query.get(id)
	return render_template('post_detail.html', article=article)


@app.route('/posts/<int:id>/del')
def delete_post(id):
	article = Article.query.get_or_404(id)
	try:
		db.session.delete(article)
		db.session.commit()
		return redirect('/posts')
	except:
		return An_error_occurred_while_deleting_the_entry()


@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def update_post(id):
	article = Article.query.get(id)
	if request.method == 'POST':
		article.title = request.form['title']
		article.intro = request.form['intro']
		article.text = request.form['text']
		try:
			db.session.commit()
			return redirect('/posts')
		except:
			return An_error_occurred_while_editing_the_article()
	else:
		return render_template('post_update.html', article=article)


@app.route('/create-article', methods=['POST', 'GET'])
def create_article():
	if request.method == 'POST':
		title = request.form['title']
		intro = request.form['intro']
		text = request.form['text']
		article = Article(title=title, intro=intro, text=text)
		try:
			db.session.add(article)
			db.session.commit()
			return redirect('/posts')
		except:
			return An_error_occurred_while_adding_an_article()
	else:
		return render_template('create_article.html')


# If error 404 ie the page was not found
# we are redirected to our page with an error.
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


if __name__ == '__main__':
	app.run(debug=True)
