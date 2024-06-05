import allure
import pytest
import requests
import data
import helper

class TestUserCreating:

    @allure.title('Успешная проверка создания нового пользователя')
    def test_register_successful_result(self, user_creating):
        payload = {
            'email': user_creating['email'],
            'password': user_creating['password'],
            'name': user_creating['name']
        }
        response = requests.post(data.user_register, data=payload)
        assert response.status_code == 200 and response.json().get("success") is True


    @allure.title('Ошибка при попытке повторного создания существующего пользователя')
    def test_register_double_user_failed_result(self, user):
        payload = {
            'email': user['email'],
            'password': user['password'],
            'name': user['name']
        }
        response = requests.post(data.user_register, data=payload)
        assert response.status_code == 403 and response.json().get("success") is False and response.json()['message'] == 'User already exists'


    @allure.title('Ошибка при создании пользователя без заполнения обязательных полей: email, password и name')
    @pytest.mark.parametrize('payload', [
        {'email': 'login@ya.ru', 'name': 'username'},
        {'email': 'login@ya.ru', 'password': 123456},
        {'password': 123456, 'name': 'username'}
    ])
    def test_register_without_one_field_failed_result(self, payload):
        response = requests.post(data.user_register, data=payload)
        assert response.status_code == 403 and response.json().get("success") is False and response.json()['message'] == 'Email, password and name are required fields'



class TestUserDataChanging:

    @allure.title('Успешная проверка изменения почты существующего пользователя')
    def test_user_changed_email_successful_result(self, user):
        new_email = helper.generate_random_login()
        payload = {'email': new_email}
        headers = {'Authorization': user['access_token']}
        response = requests.patch(data.user_info, data=payload, headers=headers)
        assert response.status_code == 200 and response.json().get("success") is True and response.json()['user']['email'] == new_email


    @allure.title('Успешная проверка изменения имени существующего пользователя')
    @pytest.mark.parametrize('name', ['new_name'])
    def test_user_changed_name_successful_result(self, user, name):
        payload = {'name': name}
        headers = {'Authorization': user['access_token']}
        response = requests.patch(data.user_info, data=payload, headers=headers)
        assert response.status_code == 200 and response.json().get("success") is True and response.json()['user']['name'] == name


    @allure.title('Успешная проверка изменения пароля существующего пользователя')
    def test_user_changed_password_successful_result(self, user):
        new_password = helper.generate_random_password()
        payload = {'password': new_password}
        headers = {'Authorization': user['access_token']}
        response = requests.patch(data.user_info, data=payload, headers=headers)
        assert response.status_code == 200 and response.json().get("success") is True


    @allure.title('Ошибка при попытке изменения почты, пароля и имени неавторизованного пользователя')
    def test_unauthorized_user_changed_datas(self):
        email = helper.generate_random_login()
        password = helper.generate_random_password()
        name = helper.generate_random_user_name(6)
        payload = {
            'email': email,
            'password': password,
            'name': name
        }
        response = requests.patch(data.user_info, data=payload)
        assert response.status_code == 401 and response.json().get("success") is False and response.json()['message'] == 'You should be authorised'




class TestUserLogin:

    @allure.title('Проверка логина существующего пользователя')
    def test_user_login_successful_login(self, user):
        payload = {
            'email': user['email'],
            'password': user['password']
        }
        response = requests.post(data.user_login, data=payload)
        assert response.status_code == 200 and response.json().get("success") is True


    @allure.title('Ошибка при проверке пользователя с некорректным логином')
    def test_login_incorrect_email_failed_result(self, user):
        payload = {
            'email': data.incorrect_email,
            'password': user['password']
        }
        response = requests.post(data.user_login, data=payload)
        assert response.status_code == 401 and response.json()['message'] == 'email or password are incorrect'and response.json().get("success") is False


    @allure.title('Ошибка при проверке пользователя с некорректным паролем')
    def test_login_incorrect_password_failed_result(self, user):
        payload = {
            'email': user['email'],
            'password': data.incorrect_password
        }
        response = requests.post(data.user_login, data=payload)
        assert response.status_code == 401 and response.json()['message'] == 'email or password are incorrect' and response.json().get("success") is False




class TestUserOrderGetting:

    @allure.title('Успешная проверка получения заказов авторизованного пользователя')
    def test_getting_order_authorized_user(self, user, order_making):
        headers = {'Authorization': user['access_token']}
        response = requests.get(data.user_order, headers=headers)
        assert response.status_code == 200 and response.json().get("success") is True and response.json()['orders'][0]['number'] == order_making


    @allure.title('Ошибка проверки получения заказов неавторизованного пользователя')
    def test_getting_order_unauthorized_user(self):
        response = requests.get(data.user_order)
        assert response.status_code == 401 and response.json().get("success") is False and response.json()['message'] == 'You should be authorised'

