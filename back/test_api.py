import requests

data = {
    'username': 'ivans',
    'password': 'qwerty'
}

r = requests.post('http://127.0.0.1:8000/api/users/login', data=data)
print(r.status_code, r.text)