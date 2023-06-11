import requests

message = f"bbbbbbbbbb"

url = "http://127.0.0.1:8001/"

# response = requests.get(url)
for i in range(1,11):
    data = {"content": f"msg{i}"}
    response = requests.post(url, json=data)
    print(response.status_code)
    print(response.json())

