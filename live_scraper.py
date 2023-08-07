import requests
from bs4 import BeautifulSoup
from match_formatter import match_formatter


live_url = 'https://www.totalcorner.com/match/today/'


response = requests.get(live_url)
soup = BeautifulSoup(response.content, 'html.parser')

match_table = soup.find('tbody', class_='tbody_match')
matches = match_table.select('tr')

matches_list = match_formatter(matches)