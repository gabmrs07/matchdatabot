import json
import os

class Bet(object):

    def __init__(self, data, matches):
        """:param min_time: O tempo mínimo da partida.
        :param max_time: O tempo máximo da partida.
        :param min_attacks: A quantidade necessária de ataques na partida.
        :param min_corners: A quantidade necessária de escanteios na partida.
        :param min_shots: A quantidade necessária de chutes na partida.
        """
        self.data = data
        self.matches = matches
        if self.key not in self.data:
            self.data[self.key] = {'WIN': 0, 'LOSE': 0}

    def get_prob(self):
        wins = self.data[self.key]['WIN']
        loses = self.data[self.key]['LOSE']
        if wins != 0:
            if loses != 0:
                rate = wins / (wins + loses)
            else:
                rate = 1
        else:
            rate = 0
        return wins, loses, rate

    def justify(self, match):

        match_id = match['match_id']
        if match_id in self.matches[self.key]:
            #print(f"match_id in matches")
            mirror = self.matches[self.key][match_id]
            if not mirror['half_finished']:
                end_corners = match['corners']
                init_corners = mirror['corners']
                if (end_corners > init_corners) and (mirror['status'] == "NULL"):
                    mirror['corner_minute'] = match['current_minutes']
                if match['half_finished']:
                    if end_corners > init_corners:
                        mirror['status'] = 'WIN'
                        self.data[self.key]['WIN'] += 1
                    else:
                        self.data[self.key]['LOSE'] += 1
                        mirror['status'] = 'LOSE'
                        mirror['corner_minute'] = 0
                    mirror['corner_diff'] = end_corners - init_corners
                    mirror['half_finished'] = True
                    print("[{}]: {} {} x {} {} | {} ESCANTEIOS | {}!".format(self.key, match['home_team'],
                                                                               match['home_score'],
                                                                               match['away_score'],
                                                                               match['away_team'],
                                                                               mirror['corner_diff'],
                                                                                mirror['status']))
