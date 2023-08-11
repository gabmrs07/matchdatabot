import math
#import unidecode
from decimal import Decimal

from telegram_message import Bot

end_times = {45, 90}
former_keys = {'home_team', 'away_team', 'league', 'finished'}
exclude_keys = {'half_finished', 'current_minutes'}
sep = '_' * 15

class Analyzer(object):
    """Salva os dados das partidas conforme o tempo requisitado."""

    handicap_set = {3, 2.5, 2, 1.75, 1.5, 1.25, 1, 0.75, 0.5, 0.25, -0.25,
                    -0.5, -0.75, -1, -1.25, -1.5, -1.75, -2, -2.5, -3}

    def __init__(self, matches):
        """Construtor inicial e cria 'analyzing', que checa se está uma análise em andamento,
        de modo que se mantenha a integridade dos dados ao se subir para o DropBox.
        :param matches: Local de arquivamento dos dados das partidas.
        """
        self.matches = matches
        self.live_matches = 0
        self.locked = False
        try:
            self.telegram = Bot(self)
            self.telegram.run_bot()
        except Exception as ex:
            print(ex, ex.args)

    def send_message(self, msg):
        try:
            self.telegram.send_message(self.telegram.updater, msg)
        except Exception as ex:
            print(ex, ex.args)

    def lock(self, n):
        """Trava o upload de dados ao DropBox.
        :param n: O número de partidas ao vivo em análise.
        """

        self.live_matches = n
        self.locked = True

    def unlock(self):
        """Destrava o upload de dados ao DropBox."""

        self.locked = False

    def checker(self, match):
        """Checa e salva os arquivos.
        :param match: Os dados retirados pelo scraper.
        """
        match_id = str(match['match_id'])
        minute = str(match['current_minutes'])
        m = self.matches.get(match_id, False)
        if math.remainder(int(minute), 5) == 0:
            if not m:
                self.matches[match_id] = {}
                m = self.matches[match_id]
                self.save_data(m, minute, match)
            elif m['finished'] == "False":
                self.save_data(m, minute, match)

    def save_data(self, data, minute, match):
        """Adiciona os dados da partida à variável matches.
        :param data: O local destinado.
        :param minute: O minuto de recorte da partida.
        :param match: Todos os dados da partida.
        """
        half_finished = (match['half_finished'] is True)
        if (minute not in end_times) or half_finished:
            for key, value in match.items():
                if key != 'match_id':
                    if key == 'handicap':
                        if key in data:
                            data[minute][key] = match[key][1]
                        else:
                            data[key] = match[key][0]
                    elif (key in former_keys) and (key not in data):
                        data[key] = match[key]
                    else:
                        if minute not in data:
                            data[minute] = {}
                        if (key not in former_keys) and (key not in exclude_keys):
                            data[minute][key] = match[key]
            if half_finished and (minute == "90"):
                data['finished'] = "True"