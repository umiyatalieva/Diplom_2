import allure
import requests
import data


class TestOrderCreating:

    @allure.title('Успешная проверка создания заказа с авторизацией пользователя')
    def test_order_successful_creating(self, user, get_ingredients):
        payload = {'ingredients': [get_ingredients[0], get_ingredients[1], get_ingredients[2]]}
        headers = {'Authorization': user['access_token']}
        response = requests.post(data.user_order, data=payload, headers=headers)
        assert response.status_code == 200 and response.json().get("success") is True and 'number' in response.json()['order'] and isinstance(response.json()['order']['number'], int)


    @allure.title('Успешная проверка создания заказа без авторизации пользователя')
    def test_orders_unauthorized_user_successful_creating(self, get_ingredients):
        payload = {'ingredients': [get_ingredients[0], get_ingredients[1], get_ingredients[2]]}
        response = requests.post(data.user_order, data=payload)
        assert response.status_code == 200 and response.json().get("success") is True and 'number' in response.json()['order'] and isinstance(response.json ()['order']['number'], int)

    @allure.title('Проверка создания заказа без ингредиентов')
    def test_orders_without_ingredients_failed(self, user):
        payload = {'ingredients': []}
        headers = {'Authorization': user['access_token']}
        response = requests.post(data.user_order, data=payload, headers=headers)
        assert response.status_code == 400 and response.json().get("success") is False and response.json()['message'] == 'Ingredient ids must be provided'


    @allure.title('Проверка создания заказа с некорректно заданным ингредиентом')
    def test_orders_wrong_ingredient_failed(self, user):
        payload = {'ingredients': ["wrong"]}
        headers = {'Authorization': user['access_token']}
        response = requests.post(data.user_order, data=payload, headers=headers)
        assert response.status_code == 500 and 'Internal Server Error' in response.text
