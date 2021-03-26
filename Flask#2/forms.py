from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    SubmitField,
    TextAreaField,
    BooleanField,
    PasswordField
)

from wtforms.validators import DataRequired, Email


class ContactForm(FlaskForm):
	email = StringField("Email: ", validators=[Email(), DataRequired()])
	password = StringField("Password: ", validators=[DataRequired()])
	submit = SubmitField("Submit")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField()

"""  
	WTForms
	WTForms – это мощная библиотека, написанная на Python и независимая от фреймворков. Она умеет генерировать формы,
	проверять их и предварительно заполнять информацией (удобно для редактирования) и многое другое. 
	Также она предлагает защиту от CSRF. Для установки WTForms используется Flask-WTF.
	Flask- WTF – это расширение для Flask, которое интегрирует WTForms во Flask. Оно также предлагает дополнительные функции,
	такие как загрузка файлов, reCAPTCHA, интернационализация (i18n) и другие. Для установки Flask-WTF нужно ввести следующую команду pip install flask-wtf
	
	
	Пакет wtform предлагает несколько классов, представляющих собой следующие поля:
	StringField, PasswordField, SelectField, TextAreaField, SubmitField
	
	
	использовать несколько валидаторов, разделив их запятыми (,). Модуль wtforms.validators предлагает базовые валидаторы,
	но их можно создавать самостоятельно. В этой форме используются два встроенных валидатора: DataRequired и Email.
	DataRequired: он проверяет, ввел ли пользователь хоть какую-информацию в поле.
	Email: проверяет, является ли введенный электронный адрес действующим.
	Введенные данные не будут приняты до тех пор, пока валидатор не подтвердит соответствие данных.

	Learn Flask#2>python app.py shell
	>>> from forms import ContactForm
	>>> from werkzeug.datastructures import MultiDict
	>>> form1 = ContactForm(MultiDict([('name', 'jerry'),('email', 'jerry@mail.com')]))
	>>> form1.validate()
	False
	>>> form1.error
	Traceback (most recent call last):
	  File "<console>", line 1, in <module>
	AttributeError: 'ContactForm' object has no attribute 'error'
	>>> form1.errors
	{'message': ['This field is required.'], 'csrf_token': ['The CSRF token is missing.']}


	Стоит обратить внимание, что данные передаются в виде объекта MultiDict, потому что функция-конструктор класса wtforms.Form принимает аргумент типа MutiDict. Если данные формы не определены при создании экземпляра объекта формы, а форма отправлена с помощью запроса POST, wtforms.Form использует данные из атрибута request.form. Стоит вспомнить, что request.form возвращает объект типа ImmutableMultiDict. Это то же самое, что и MultiDict, но он неизменяемый.

	Метод validate() проверяет форму. Если проверка прошла успешно, он возвращает True, если нет — False.

	>>>
	>>> form1.validate()
	False
	>>>
	Форма не прошла проверку, потому что обязательному полю message при создании объекта формы 
	не было передано никаких данных. Получить доступ к ошибкам форм можно с помощью атрибута 
	errors объекта формы:

	>>>
	>>> form1.errors
	{'message': ['This field is required.'], 'csrf_token': ['The CSRF token is missing.']}
	>>>
	Нужно обратить внимание, что в дополнение к сообщению об ошибке для поля message, вывод также 
	содержит сообщение об ошибке о недостающем csfr-токене. Это из-за того что в данных формы нет 
	запроса POST с csfr-токеном.

	Отключить CSFR-защиту можно, передав csfr_enabled=False при создании экземпляра класса формы. Пример:
	
	>>> form3 = ContactForm(MultiDict([('name', 'spike'),('email', 'spike@mail.com')]), csrf_enabled=False)
	>>>
	>>> form3.validate()
	False
	>>>
	>>> form3.errors
	{'message': ['This field is required.']}
"""
