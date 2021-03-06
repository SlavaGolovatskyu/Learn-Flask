from typing import List

def check_len_password_user(password: str) -> bool:
	return len(password) > 6


def check_len_email_user(email: str) -> bool:
	return len(email) < 50


def return_error_message(email: bool, password: bool) -> str:
	if not email and not password:
		return ("У вас слишком большая длинна email-почты," 
			    " а также слишком маленький пароль")

	if not email and password:
		return 'Слишком большая длинна email-почты'

	if email and not password:
		return 'Слишком маленькая длинна пароля'


def check_len_all_data(email: str, password: str) -> List[bool]:
	len_email = check_len_email_user(email)
	len_password = check_len_password_user(password)
	return [len_email, len_password]


