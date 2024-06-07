import allure
import requests
import data


class TestOrderCreating:

    @allure.title('Успешная проверка создания заказа с авторизацией пользователя')
    def test_order_successful_creating(self, user, get_ingredients):
        payload = {'ingredients': [get_ingredients[0], get_ingredients[1], get_ingredients[2]]}
        headers = {'Authorization': user['access_token']}
        response = requests.post(data.user_order, data=payload, headers=headers)
        assert response.status_code == 200 and response.json().get("success") is True


    @allure.title('Успешная проверка создания заказа без авторизации пользователя')
    def test_orders_unauthorized_user_successful_creating(self, get_ingredients):
        payload = {'ingredients': [get_ingredients[0], get_ingredients[1], get_ingredients[2]]}
        response = requests.post(data.user_order, data=payload)
        assert response.status_code == 200 and response.json().get("success") is True

    @allure.title('Проверка создания заказа без ингредиентов')
    def test_orders_without_ingredients_failed(self, user):
        payload = {'ingredients': []}
        headers = {'Authorization': user['access_token']}
        response = requests.post(data.user_order, data=payload, headers=headers)
        assert response.status_code == 400  and response.json()['message'] == 'Ingredient ids must be provided'


    @allure.title('Проверка создания заказа с некорректно заданным ингредиентом')
    def test_orders_wrong_ingredient_failed(self, user):
        payload = {'ingredients': ["wrong"]}
        headers = {'Authorization': user['access_token']}
        response = requests.post(data.user_order, data=payload, headers=headers)
        assert response.status_code == 500 and 'Internal Server Error' in response.text
class TestUserOrderGetting:
    @allure.title('Успешная проверка получения заказов авторизованного пользователя')
    def test_getting_order_authorized_user(self, user, order_making):
        headers = {'Authorization': user['access_token']}
        response = requests.get(data.user_order, headers=headers)
        assert response.status_code == 200 and response.json()['orders'][0]['number'] == order_making



    @allure.title('Ошибка проверки получения заказов неавторизованного пользователя')
    def test_getting_order_unauthorized_user(self):
        response = requests.get(data.user_order)
        assert response.status_code == 401 and response.json()['message'] == 'You should be authorised'

