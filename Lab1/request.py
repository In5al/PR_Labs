import requests

data = requests.post("http://127.0.0.1:5000/hello", json = {"Carp":"Dan-Octavian"})
print("Status Code", data.status_code)
print("JSON Response ", data.text)