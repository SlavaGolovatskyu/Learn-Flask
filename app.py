from datetime import datetime
from flask import Flask, render_template, url_for, request, redirect
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
@app.route('/home')
def home_page():
	return render_template('index.html')


@app.route('/sign-in', methods=['POST', 'GET'])
def sign_in():
	if request.method == 'POST':
		pass
	else:
		return render_template('sign_in.html')


@app.route('/sign-up', methods=['POST', 'GET'])
def sign_up():
	if request.method == 'POST':
		pass
	else:
		return render_template('sign_up.html')


@app.route('/about')
def about_page():
	return render_template('about.html')


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
		return 'При удалении записи произошла ошибка'


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
			return 'При редактировании статьи произошла ошибка'
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
			return 'При добавлении статьи произошла ошибка'
	else:
		return render_template('create_article.html')


# If error 404 ie the page was not found
# we are redirected to our page with an error.
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


if __name__ == '__main__':
	app.run(debug=True)