import requests #testing the requests to the server  
  
base = "http://localhost:5000/"
response = requests.put(base + "DataBase/" + str(2), {"Name": "Omer", "Phone": "0506498555"})
print(response)
print(response.json())
response = requests.get(base + "DataBase/" + str(2))
print(response)
print(response.json())
response = requests.get(base + "DataBase/" + str(3))
print(response.content)
response = requests.put(base + "DataBase/" + str(3), {"Name": "Omer", "Phone": "0506498555"})
response = requests.put(base + "DataBase/" + str(4), {"Name": "Omer", "Phone": "0506498555"})
response = requests.get(base + "DataBase/" + str(2))
print(response)
print(response.json())
  