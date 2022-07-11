import requests

#POST先URL
url = "http://127.0.0.1:8000"

#JSON形式のデータ
payload = {'some': 'data'}
r = requests.post(url, json=payload)
print(r)
