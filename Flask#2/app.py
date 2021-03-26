import json

from flask import (
	Flask, 
	render_template, 
	url_for, 
	request, 
	redirect, 
	request,
	flash, 
	make_response,
	session
)

from flask_login import (
	LoginManager, 
	UserMixin,
	login_required,
	login_user, 
	current_user
)

from forms import ContactForm, LoginForm
from datetime import datetime
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from werkzeug.security import generate_password_hash, check_password_hash

# Мы можем изменить путь к templates например если у нас папка с другим именем
# Мы просто делаем вот так: app = Flask(__name__, template_folder="jinja_templates")
# Так же можем сделать и с папкой static app = Flask(__name__, static_folder="static_dir")


"""
	Установка SECRET_KEY
	По умолчанию Flask-WTF предотвращает любые варианты CSFR-атак. 
	Это делается с помощью встраивания специального токена в скрытый элемент 
	<input> внутри формы. Затем этот токен используется для проверки подлинности запроса.
	До того как Flask-WTF сможет сгенерировать csrf-токен, необходимо добавить секретный ключ.
	Установить его в файле main2.py необходимо следующим образом:

	#...
	app.debug = True
	app.config['SECRET_KEY'] = 'a really really really really long secret key'

	manager = Manager(app)
	#...

	Секретный ключ должен быть строкой — такой, которую сложно разгадать и,
	желательно, длинной. SECRET_KEY используется не только для создания CSFR-токенов.
	Он применяется и в других расширениях Flask. Секретный ключ должен быть безопасно сохранен. 
	Вместо того чтобы хранить его в приложении, лучше разместить в переменной окружения. 
	О том как это сделать — будет рассказано в следующих разделах.
"""

SECRET_KEY = json.load(open('secret_key.json', 'r'))

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY['secret_key']
app.debug = True
app.reload = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)
mail = Mail(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'



class User(db.Model, UserMixin):
	__tablename__ = 'users'
	id = db.Column(db.Integer(), primary_key=True)
	name = db.Column(db.String(100))
	username = db.Column(db.String(50), nullable=False, unique=True)
	email = db.Column(db.String(100), nullable=False, unique=True)
	password_hash = db.Column(db.String(100), nullable=False)
	created_on = db.Column(db.DateTime(), default=datetime.utcnow)
	updated_on = db.Column(db.DateTime(), default=datetime.utcnow,  onupdate=datetime.utcnow)

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	def __repr__(self):
		return "<{}:{}>".format(self.id, self.username)

@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)


"""
	* Flask предлагает три варианта для создания ответа:
	* В виде строки или с помощью шаблонизатора
	* Объекта ответа
	* Кортежа в формате (response, status, headers) или (response, headers)
	* Далее о каждом поподробнее.
"""


"""
@app.route('/visits-counter/')
def visits():
    if 'visits' in session:
		session['visits'] = session.get('visits') + 1  # чтение и обновление данных сессии
    else:
		session['visits'] = 1  # настройка данных сессии
    	return "Total visits: {}".format(session.get('visits'))

@app.route('/delete-visits/')
def delete_visits():
    session.pop('visits', None)  # удаление данных о посещениях
    return 'Visits deleted'
"""


"""
Доступ к куки
Для доступа к куки используется атрибут cookie объекта request. 
cookie — это атрибут типа словарь, содержащий все куки, отправленные браузером.
"""
@app.route('/cookie/')
def cookie():
	if not request.cookies.get('foo'):
		res = make_response("Setting a cookie")
		res.set_cookie('foo', 'bar', max_age=60*60*24*365*2)
	else:
		res = make_response("Value of cookie foo is {}".format(request.cookies.get('foo')))
		return res

"""
@app.route('/login/', methods=['get', 'post'])
def login():
	form = ContactForm()
	if form.validate_on_submit():
			Поля формы, определенные в классе формы становятся атрибутами объекта формы. 
			Чтобы получить доступ к данным поля используется атрибут data поля формы:

			form.name.data  # доступ к данным в поле name.
			form.email.data  # доступ к данным в поле email.
			Чтобы получить доступ ко всем данные формы сразу нужно использовать атрибут data к объекту формы:
			form.data  # доступ ко всем данным
			Если использовать запрос GET при посещении /contact/, метод validate_on_sumbit() 
			вернет False. Код внутри if будет пропущен, а пользователь получит пустую HTML-форму.
		email = form.email.data
		password = form.password.data
		print(email)
		print(password)
		# здесь логика базы данных
		print("\nData received. Now redirecting ...")
		flash("Sign in passed success", "success")
		return redirect(url_for('login'))
	return render_template('login.html', form=form)
"""


@app.route('/admin/')
@login_required
def admin():
    return render_template('admin.html')


@app.route('/login/', methods=['post', 'get'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = db.session.query(User).filter(User.username == form.username.data).first()
		if user and user.check_password(form.password.data):
			login_user(user, remember=form.remember.data)
			return redirect(url_for('admin'))

		flash("Invalid username/password", 'error')
		return redirect(url_for('login'))
	return render_template('login.html', form=form)


@app.route('/')
def index():
	return render_template('index.html')


if __name__ == '__main__':
	manager.run()