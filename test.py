import requests

url = "http://127.0.0.1:8000/tasks"
response = requests.get(url)
data = response.json()

print(data)
