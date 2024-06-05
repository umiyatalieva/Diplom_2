import random
import string


# методы генерируют строки для создания необходимых переменных для тестирования
def generate_random_user_name(length):
    letters = string.ascii_lowercase
    random_user_name = ''.join(random.choice(letters) for i in range(length))
    return random_user_name

def generate_random_login():
    random_number = random.randint(100, 999)
    email = f'{random_number}@ya.ru'
    return email

def generate_random_password():
    password = random.randint(1000000, 9999999)
    return password

