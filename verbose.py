from datetime import datetime


sep = '_' * 35


class Verbose(object):

    def __init__(self):
        #self.telegram_bot = Bot()
        #self.telegram_bot.run_bot()
        self.count = 0
        self.tips = []
        self.telegram_tips = []
        print("\nCornerBotApp iniciando...")

    def start(self):
        """Inicia a contagem da análise das partidas."""

        self.call_sep()
        print('ANALIZANDO:')
        self.call_sep()

    def add_tip(self, match):
        pass

    def match_count(self, n, total):
        """Realiza a contagem das análises.
        :param n: O número da partida atual da análise.
        :param total: O número total das partidas a ser analizada.
        """
        print(f"{n} de {total} partidas...")

    def call_sep(self):
        """Chama uma separação."""

        print(f"\n{sep}\n\n")

    def end(self, dt, matches):
        """Finaliza uma rodada.
        :param dt: datetime do último upload de matches.json.
        """
        dt = 'Não houve' if dt is None else dt.strftime('%H:%M:%S | %d/%m/%y')
        self.count += 1
        print(f"Rodada atual: {self.count}\nPartidas analisadas: {len(matches)}\nÚltimo upload: {dt}.")
        self.call_sep()
        print(f"Próxima rodada em 30 segundos...\n\n")
