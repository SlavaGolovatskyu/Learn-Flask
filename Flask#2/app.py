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

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from forms import ContactForm
from flask_script import Manager

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
migrate = Migrate(app,  db)
manager.add_command('db', MigrateCommand)


class Account(db.Model):
	user_id = db.Column(db.Integer, primary_key = True)
	email = db.Column(db.String(50), nullable = False)
	password = db.Column(db.String(100), nullable = False)
	date_reg = db.Column(db.DateTime, default = datetime.utcnow)
	ttt = db.Column(db.Integer, default = 1)
	ttt1 = db.Column(db.Integer, default = 2)
	def __repr__(self):
		return '<Account %r>' % self.user_id

class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    designation = db.Column(db.String(255), nullable=False)
    doj = db.Column(db.Date(), nullable=False)


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


@app.route('/login/', methods=['get', 'post'])
def login():
	form = ContactForm()
	if form.validate_on_submit():
		"""
			Поля формы, определенные в классе формы становятся атрибутами объекта формы. 
			Чтобы получить доступ к данным поля используется атрибут data поля формы:

			form.name.data  # доступ к данным в поле name.
			form.email.data  # доступ к данным в поле email.
			Чтобы получить доступ ко всем данные формы сразу нужно использовать атрибут data к объекту формы:
			form.data  # доступ ко всем данным
			Если использовать запрос GET при посещении /contact/, метод validate_on_sumbit() 
			вернет False. Код внутри if будет пропущен, а пользователь получит пустую HTML-форму.
		"""
		email = form.email.data
		password = form.password.data
		print(email)
		print(password)
		# здесь логика базы данных
		print("\nData received. Now redirecting ...")
		flash("Sign in passed success", "success")
		return redirect(url_for('login'))
	return render_template('login.html', form=form)


@app.route('/')
def index():
	return render_template('index.html')


if __name__ == '__main__':
	manager.run()