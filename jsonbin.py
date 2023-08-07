import requests
import json

bin_id = '631d1d4e5c146d63ca96d344'
api_key = '$2b$10$4942xf3rFGj3hnh8JRiNZOo0l0KLbY6rHPx7JSQiNWKScmWdd6gWK'

def get_json(bin_id):
    url = f'https://api.jsonbin.io/v3/b/{bin_id}/latest'
    headers = {'X-Master-Key': api_key}
    req = requests.get(url, json=None, headers=headers)
    return {}
    #return json.loads(req.text)['record']


def update_json(bin_id, data):
    url = f'https://api.jsonbin.io/v3/b/{bin_id}'
    headers = {'Content-Type': 'application/json', 'X-Master-Key': api_key}
    req = requests.put(url, json=data, headers=headers)
    return req.status_code

def reset_data():
 #   matches_update = update_json('631d3009e13e6063dca36ca8', {'date_created': '10/09/2022'})
    bet_update = update_json('631d30185c146d63ca96e3ad', {'date_created': '10/09/2022'})

if __name__ == '__main__':
    reset_data()