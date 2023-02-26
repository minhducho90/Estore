# import json
# import urllib.request


# url = urllib.request.urlopen("https://fakestoreapi.com/products/1/")
# url = urllib.request.urlopen("http://maps.googleapis.com/maps/api/geocode/json?address=google")
# data = json.loads(url.read().decode())

# print(data)

# application/json
# text/json

import requests
import json

url_api = "https://fakestoreapi.com/products/1/"
# data = requests.get(url_api)
#Cach 1:
# data = json.loads(requests.get(url_api))
# print(data)
#Cach 2:
data = requests.get(url_api).json()
print(data)
title = data['title']
print(title)
description = data.get('description', 'Not available')
print(description)
public_day = data.get('public_day', '2023-01-15')
print(public_day)
# try:
#     public_day1 = data['public_day']
# except KeyError:
#     print("Not available")
