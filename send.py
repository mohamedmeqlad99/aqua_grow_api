import requests

url = "http://127.0.0.1:5000/api/recommendation"
data = {
    "crop": "corn"
}

response = requests.post(url, json=data)
print(response.status_code)
print(response.json())
