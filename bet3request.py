import requests

url = "https://www.bet365.com/#/IP/B1"
r = requests.get(url)
print(r.text)