sep = '_' * 35


class Verbose(object):

    def __init__(self):
        self.count = 0
        self.last_upload_time = None
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

    def get_stats(self, matches):
        """Gera as estatisticas das partidas analisadas.
        :param matches: data das partidas.
        """
        dt = self.last_upload_time
        dt = 'Não houve' if dt is None else dt.strftime('%H:%M:%S | %d/%m/%y')
        finished = [match_id for match_id, match in matches.items() if match['finished'] == 'True']
        content = f"Rodada atual: {self.count}"\
              f"\nPartidas analisadas: {len(matches)}"\
              f"\nPartidas encerradas: {len(finished)}"\
              f"\nÚltimo upload: {dt}."
        return content

    def telegram_info(self, analyzer):
        """Gera as estatisticas das partidas analisadas.
        :param dt: datetime do último upload de matches.json.
        :param matches: instância da classe Analyzer.
        """
        msg = f"Cornerbot Info:\n\n{self.get_stats(analyzer.matches)}\n\n" \
              f"Partidas em análise: {analyzer.live_matches}"
#        analyzer.send_message(msg)

    def end(self, dt, matches):
        """Finaliza uma rodada.
        :param dt: datetime do último upload de matches.json.
        :param matches: data das partidas.
        """
        self.last_upload_time = dt
        self.count += 1
        print(self.get_stats(matches))
        self.call_sep()
        print(f"Próxima rodada em 30 segundos...\n\n")
