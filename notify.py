import unidecode

sep = '_' * 35


class Analyzer(object):
    """Salva os dados das partidas conforme o tempo requisitado."""

    def __init__(self, matches, times):
        """:param matches: Local de arquivamento dos dados das partidas.
        :param times: O tempo de recorte dos dados das partidas.
        """
        self.matches = matches
        self.times = times

    def checker(self, match):

        current_time = match['current_minutes']
        match_id = match['match_id']
        attacks = match['attacks']
        corners = match['corners']
        shots = match['shots']
        half_finished = match['half_finished']
        score_diff = match['home_score'] - match['away_score']
        key = self.get_key(attacks, corners, shots)
        if score_diff == 0:  # Se empate
            side = 'Draw'
        elif score_diff > 0:  # Se vitória do time da casa
            side = 'Home'
        elif score_diff < 0:  # Se vitória do time visitante
            side = 'Away'
        home_ascii = unidecode.unidecode(match['home_team']).replace(' ', '/')
        site = f'https://www.bet365.com/#/AX/K^{home_ascii}/'
        tip = "{} | {} | {}'\n{} {} x {} {}\nA: {} ({}) {} | C: {} ({}) {} | S: {} ({}) {}\n\n{}".format(
            key,
            side,
            current_time,
            match['home_team'],
            match['home_score'],
            match['away_score'],
            match['away_team'],
            match['home_attack'],
            attacks,
            match['away_attack'],
            match['home_corner'],
            corners,
            match['away_corner'],
            match['home_shot'],
            shots,
            match['away_shot'],
            site)
        if (current_time == 45) and half_finished:
            if match_id in self.data:
                mirror = self.data[match_id]
                if not mirror['half_finished']:
                    self.justify(match, mirror)
                    del self.data[match_id]
        elif (self.min_time <= current_time <= self.max_time):
            if self.strategies:
                if (match_id not in self.notified):
                    for args_key, t_prob in self.strategies.items():
                        args = args_key.split('-')
                        a = int(args[0])
                        c = int(args[1])
                        s = int(args[2])
                        if (attacks >= a) and (corners >= c) and (shots >= s):
                            self.t_tips.append(f"S-{args_key} | {tip}\n{sep}\n\n")
                            self.notified.add(match_id)
                            t_prob['MATCHES'].add(match_id)
            if current_time >= 39:
                self.save_match(key, match, match_id)
            return tip
        elif match_id in self.data:
            return f"{tip} ..."
        else:
            return False

    def save_match(self, key, match, match_id):
        if match_id not in self.data:
            match['key'] = key
            self.data[match_id] = match

    def justify(self, match, mirror):
        key = mirror['key']
        end_corners = match['corners']
        init_corners = mirror['corners']
        if key not in self.prob:
            self.prob[key] = {'WIN': 0, 'LOSE': 0}
        if (end_corners > init_corners) and (mirror['status'] == "NULL"):
            mirror['corner_minute'] = match['current_minutes']
            mirror['status'] = 'WIN'
            self.prob[key]['WIN'] += 1
            for s_args, t_prob in self.strategies.items():
                if match['match_id'] in t_prob['MATCHES']:
                    t_prob['WIN'] += 1
                    t_prob['STREAK'] += 1
                    if t_prob['BEST STREAK'] < t_prob['STREAK']:
                        t_prob['BEST STREAK'] = t_prob['STREAK']
                    if t_prob['WORST STREAK'] > t_prob['STREAK']:
                        t_prob['WORST STREAK'] = t_prob['STREAK']
                    t_prob['MATCHES'].remove(match['match_id'])
                    self.t_just.append("\n[{}]: {} {} x {} {} | {} ESCANTEIOS | {}!\n{}\n\n".format(s_args,
                                                                                                    match['home_team'],
                                                                                                    match['home_score'],
                                                                                                    match['away_score'],
                                                                                                    match['away_team'],
                                                                                                    mirror[
                                                                                                        'corner_diff'],
                                                                                                    mirror['status'],
                                                                                                    sep))
        else:
            mirror['corner_minute'] = 0
            mirror['status'] = 'LOSE'
            self.prob[key]['LOSE'] += 1
            for s_args, t_prob in self.strategies.items():
                if match['match_id'] in t_prob['MATCHES']:
                    t_prob['LOSE'] -= 1
                    t_prob['STREAK'] -= 1
                    if t_prob['BEST STREAK'] < t_prob['STREAK']:
                        t_prob['BEST STREAK'] = t_prob['STREAK']
                    if t_prob['WORST STREAK'] > t_prob['STREAK']:
                        t_prob['WORST STREAK'] = t_prob['STREAK']
                    t_prob['MATCHES'].remove(match['match_id'])
                    self.t_just.append("\n[{}]: {} {} x {} {} | {} ESCANTEIOS | {}!\n{}\n\n".format(s_args,
                                                                                                    match['home_team'],
                                                                                                    match['home_score'],
                                                                                                    match['away_score'],
                                                                                                    match['away_team'],
                                                                                                    mirror[
                                                                                                        'corner_diff'],
                                                                                                    mirror['status'],
                                                                                                    sep))
        mirror['corner_diff'] = end_corners - init_corners
        mirror['half_finished'] = True
        self.justified = "\n[{}]: {} {} x {} {} | {} ESCANTEIOS | {}!".format(key,
                                                                              match['home_team'],
                                                                              match['home_score'],
                                                                              match['away_score'],
                                                                              match['away_team'],
                                                                              mirror['corner_diff'],
                                                                              mirror['status'])
