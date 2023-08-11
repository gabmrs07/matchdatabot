import requests
import time

from bs4 import BeautifulSoup
from datetime import datetime
from threading import Thread

from analyzer import Analyzer
from db import DropBox
from match_formatter import match_formatter
from verbose import Verbose

count = 1
dt_upload = None
live_url = 'https://www.totalcorner.com/match/today/'
ended_url = 'https://www.totalcorner.com/match/today/ended'


#def notify(analyzer, verbose, seconds=3600):
  #  while True:
 #       time.sleep(seconds)
#        verbose.telegram_info(analyzer)

def background_ended_matches(analyzer, seconds=600):
    while True:
        time.sleep(seconds)
        try:
            data = analyzer.matches
            response = requests.get(ended_url, headers = {
                'User-Agent': 'Popular browser\'s user-agent',})
            soup = BeautifulSoup(response.content, 'html.parser')
            match_table = soup.find('tbody', class_='tbody_match')
            matches_list = []
            for match in match_formatter(match_table.select('tr')):
                match_id = str(match['match_id'])
                if match_id in data:
                    if data[match_id]["finished"] == "False":
                        matches_list.append(match)
            for match in matches_list:
                analyzer.checker(match)
            print(f'Partidas encerradas analisadas: {len(matches_list)}')
        except Exception as ex:
            ex_msg = f"Um erro ocorreu ao pegar as partidas em TotalCorner[Finished]: \nException: {ex}\n{ex.args}\n"
            print(ex_msg)
            print("Nova tentativa em 30 segundos...")
            time.sleep(30)
            continue

def background_upload(db, data, analyzer, seconds=300):
    """Sobe os arquivos sem interromper o loop principal.
    :param db: O objeto de controle do DropBox.
    :param matches: Os dados json que serão subidos ao DropBox.
    :param analyzer: Instância de Analyzer, para controle dos uploads.
    :param seconds: O tempo de intervalo.
    """
    retry = False
    while True:
        if not retry:
            time.sleep(seconds)
        if analyzer.locked:
            retry = True
            time.sleep(30)
        else:
            try:
                global dt_upload
                db.upload('matches.json', matches, '/matchdata', mode='overwrite')
                dt_upload = datetime.now()
                retry = False
            except Exception as ex:
                retry = True
                print(data)
                print(f"O arquivo 'matches.json' não pode ser subido.\nException: {ex}\n{ex.args}\n")
                print("Nova tentativa em 30 segundos...")


if __name__ == '__main__':

    matches = {}
    while True:
        try:
            dbox = DropBox('pHpPgE8H-T8AAAAAAAAAASLRzBIjEtV0_FBWgxsxL87389YY9e4ZpOJKeBH1OXav')
            matches = dbox.download('matches.json', '/matchdata')
            break
        except Exception as ex:
            if str(ex.args[1]) == "DownloadError('path', LookupError('not_found', None))":
                matches = {}
                break
            print(f"O arquivo 'matches.json' não pode ser baixado.\nException: {ex}\n{ex.args}\n")
            print("Nova tentativa em 30 segundos...")
            continue

    analyzer = Analyzer(matches)
    upload_thread = Thread(target=background_upload, args=[dbox, matches, analyzer])
    upload_thread.start()
    ended_thread = Thread(target=background_ended_matches, args=[analyzer])
    ended_thread.start()
    verb = Verbose()
#    telegram_info_thread = Thread(target=notify, args=[analyzer, verb])
 #   telegram_info_thread.start()

    while True:
        try:
            response = requests.get(live_url, headers = {
                'User-Agent': 'Popular browser\'s user-agent',})
            soup = BeautifulSoup(response.content, 'html.parser')
            match_table = soup.find('tbody', class_='tbody_match')
            matches_list = match_formatter(match_table.select('tr'))
        except Exception as ex:
            ex_msg = f"Um erro ocorreu ao pegar as partidas em TotalCorner: \nException: {ex}\n{ex.args}\n"
            print(ex_msg)
            print("Nova tentativa em 30 segundos...")
            time.sleep(30)
            continue

        matches_length = len(matches_list)
        analyzer.lock(matches_length)
        verb.start()
        for n, match in enumerate(matches_list, 1):
            verb.match_count(n, matches_length)
            analyzer.checker(match)
        analyzer.unlock()
        verb.call_sep()
        verb.end(dt_upload, matches)
        time.sleep(30)