import requests

data = {
    'auth_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NywiZXhwIjoxNzkyOTIxMjQzfQ.J8ehI446GzdMEHyhy-L-_KM4241rU6C-UgRg78rJAEI'
}

r = requests.get('https://onatdf-83-234-174-96.ru.tuna.am/')
print(r.status_code, r.text)