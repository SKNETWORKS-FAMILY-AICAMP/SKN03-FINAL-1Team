import requests

url = 'https://api.documento.click/papers/search/'
headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
}
data = {
    'userKeyword': 'test'
}

response = requests.post(url, headers=headers, json=data)

print("Status Code:", response.status_code)
print("Response:", response.json())
