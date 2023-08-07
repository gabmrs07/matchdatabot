from collections import defaultdict
from decimal import Decimal as Dc

from statistics import *

from db import DropBox


args = [('19', '30'), ('34', '45'), ('39', '45'), ('59', '70'), ('69', '80')]
dbox = DropBox('pHpPgE8H-T8AAAAAAAAAASLRzBIjEtV0_FBWgxsxL87389YY9e4ZpOJKeBH1OXav')
matches = dbox.download('matches.json', '/corner')
strategies = dbox.download('strategies.json', '/corner')

keys_to_save = {'attacks', 'corners', 'shots'}
prob = {}

def clean_data():
    for match_id, match_data in matches.copy().items():
        for (init_time, final_time) in args:
            if not (init_time in match_data) or not (final_time in match_data):
                if init_time in match_data:
                    del matches[match_id][init_time]
                elif final_time in match_data:
                    del matches[match_id][final_time]
        if len(match_data.keys()) == 3:
            del matches[match_id]
    dbox.upload('matches.json', matches, '/corner', mode='overwrite')

def get_statistics():
    for arg in args:
        prob[arg] = defaultdict(int)
        for status in {'win', 'lose'}:
            prob[arg][status] = defaultdict(int)
            for key in keys_to_save:
                prob[arg][status][f'{key}_list'] = []

    for match in matches.values():

        for (init_time, final_time) in args:
            arg = (init_time, final_time)

            if (init_time in match) and (final_time in match):
                init = match[init_time]
                final = match[final_time]
                i_corner = init['corners']
                f_corner = final['corners']
                streak = prob[arg]['streak']
                if f_corner > i_corner:
                    if init_time == '34':
                        diff = f_corner - i_corner
                        if diff > 1:
                            prob[arg]['win_times'] += 1
                    else:
                        prob[arg]['win_times'] += 1
                    if streak >= 0:
                        prob[arg]['streak'] += 1
                    else:
                        if streak < prob[arg]['worst']:
                            prob[arg]['worst'] = streak
                        prob[arg]['streak'] = 1
                    for key in keys_to_save:
                        prob[arg]['win'][key] += init[key]
                        prob[arg]['win'][f"{key}_list"].append(init[key])
                else:
                    prob[arg]['lose_times'] += 1
                    if streak <= 0:
                        prob[arg]['streak'] -= 1
                    else:
                        if streak > prob[arg]['best']:
                            prob[arg]['best'] = streak
                        prob[arg]['streak'] = -1
                    prob[arg]['streak'] = prob[arg]['streak'] - 1
                    for key in keys_to_save:
                        prob[arg]['lose'][key] += init[key]
                        prob[arg]['lose'][f"{key}_list"].append(init[key])

    for arg in args:
        p = prob[arg]
        wins = p['win_times']
        loses = p['lose_times']
        sample = wins + loses
        rate = wins / sample
        w_attacks = p['win']['attacks_list']
        w_corners = p['win']['corners_list']
        w_shots = p['win']['shots_list']
        l_attacks = p['lose']['attacks_list']
        l_corners = p['lose']['corners_list']
        l_shots = p['lose']['shots_list']
        wm_attacks = mean(w_attacks)
        wm_corners = mean(w_corners)
        wm_shots = mean(w_shots)
        lm_attacks = mean(l_attacks)
        lm_corners = mean(l_corners)
        lm_shots = mean(l_shots)
        wdp_attacks = pstdev(w_attacks)
        wdp_corners = pstdev(w_corners)
        wdp_shots = pstdev(w_shots)
        ldp_attacks = pstdev(l_attacks)
        ldp_corners = pstdev(l_corners)
        ldp_shots = pstdev(l_shots)
        print("{}\n\nAmostra: {} | Wins: {} | Loses: {}\n\
    Win Rate: {:.2%} | Win Odd: {:.3}\n\
    Lose Rate: {:.2%} | Lose Odd: {:.3}\n\
    Streak: {} | Best: {} | Worst: {}\n".format(
                                                                arg,
                                                                sample,
                                                                wins,
                                                                loses,
                                                                rate,
                                                                1/rate,
                                                                1-rate,
                                                                1/(1-rate),
                                                                p['streak'],
                                                                p['best'],
                                                                p['worst']))
        print("W | Média | Ataques: {:.2f} | Escanteios: {:.2f} | Chutes: {:.2f}".format(
                                                                                wm_attacks,
                                                                                wm_corners,
                                                                                wm_shots))
        print("L | Média | Ataques: {:.2f} | Escanteios: {:.2f} | Chutes: {:.2f}\n".format(
                                                                                lm_attacks,
                                                                                lm_corners,
                                                                                lm_shots))
        print("W | Moda | Ataques: {} | Escanteios: {} | Chutes: {}".format(
                                                                                mode(w_attacks),
                                                                                mode(w_corners),
                                                                                mode(w_shots)))
        print("L | Moda | Ataques: {} | Escanteios: {} | Chutes: {}\n".format(
                                                                                mode(l_attacks),
                                                                                mode(l_corners),
                                                                                mode(l_shots)))
        print("W | Variância | Ataques: {:.2f} | Escanteios: {:.2f} | Chutes: {:.2f}".format(
                                                                                pvariance(w_attacks),
                                                                                pvariance(w_corners),
                                                                                pvariance(w_shots)))
        print("L | Variância | Ataques: {:.2f} | Escanteios: {:.2f} | Chutes: {:.2f}\n".format(
                                                                                pvariance(l_attacks),
                                                                                pvariance(l_corners),
                                                                                pvariance(l_shots)))
        print("W | Desvio Padrão | Ataques: {:.2f} | Escanteios: {:.2f} | Chutes: {:.2f}".format(
                                                                                wdp_attacks,
                                                                                wdp_corners,
                                                                                wdp_shots))
        print("L | Desvio Padrão | Ataques: {:.2f} | Escanteios: {:.2f} | Chutes: {:.2f}\n".format(
                                                                                ldp_attacks,
                                                                                ldp_corners,
                                                                                ldp_shots))
        print("W | Coef. de Variação | Ataques: {:.2%} | Escanteios: {:.2%} | Chutes: {:.2%}".format(
                                                                                wdp_attacks / wm_attacks,
                                                                                wdp_corners / wm_corners,
                                                                                wdp_shots / wm_shots))
        print("L | Coef. de Variação | Ataques: {:.2%} | Escanteios: {:.2%} | Chutes: {:.2%}\n\n\n".format(
                                                                                ldp_attacks / lm_attacks,
                                                                                ldp_corners / lm_corners,
                                                                                ldp_shots / lm_shots))

def strategies_view():
    for n, (s_key, s_values) in enumerate(strategies.items(), 1):
        msg = "S{}-{} | A: {} | R$ {:.2f} | STREAK: {:+} | {:+} | {:+}\n".format(n, s_key,
                                                                 len(s_values['match_ids']),
                                                                 s_values['bank'],
                                                                 s_values.get('streak', 0),
                                                                 s_values.get('best', 0),
                                                                 s_values.get('worst', 0))
        print(msg)


def s1(t1, t2, a1, c1, s1, hand_set, a2=0, c2=0, s2=0):
    keys_to_save = {'attacks', 'corners', 'shots', 'handicap'}
    arg = (t1, t2)
    prob[arg] = defaultdict(Dc)
    for status in {'win', 'lose'}:
        prob[arg][status] = defaultdict(Dc)
        for key in keys_to_save:
            prob[arg][status][f'{key}_list'] = []

    for match in matches.values():
        if (t1 in match) and (t2 in match):

            handicap = Dc(match['handicap'])
            diff = match[t1]['home_score'] - match[t1]['away_score']
            init = match[t1]
            final = match[t2]
            i_corner = init['corners']
            f_corner = final['corners']
            atk = init['attacks']
            cnr = init['corners']
            sht = init['shots']
            streak = prob[arg]['streak']


            attack = (a1 <= atk) if (a2 == 0) else (a1 <= atk <= a2)
            corner = (c1 <= cnr) if (c2 == 0) else (c1 <= cnr <= c2)
            shot = (s1 <= sht) if (s2 == 0) else (s1 <= sht <= s2)

            home_hand = handicap
            away_hand = handicap * -1

            home_score = match[t1]['home_score']
            away_score = match[t1]['away_score']
            home_diff = ((home_score + home_hand) > 0)
            away_diff = ((away_score + away_hand) > 0)
            fav_lost = True if ((home_diff and not away_diff) or (not home_diff and away_diff)) else False
            hand_range = True if ((home_hand in hand_set) or (away_hand in hand_set)) else False

            if all([attack, corner, shot, diff != 0, diff in {1, -1}, fav_lost, hand_range]):
#                print("Hand. H e A: {} , {} | {} x {} | Diff: {} | Hand. Score H e A: {} x {}".format(
 #               home_hand, away_hand, home_score, away_score, diff, home_diff, away_diff, hand_range))
                if (f_corner > i_corner):

                    prob[arg]['win_times'] += 1
                    if streak >= 0:
                        prob[arg]['streak'] += 1
                    else:
                        if streak < prob[arg]['worst']:
                            prob[arg]['worst'] = streak
                        prob[arg]['streak'] = 1
                    for key in keys_to_save:
                        if key in init:
                            n = Dc(str(init[key]).strip('\t').strip(')'))
                            prob[arg]['win'][key] += n
                            prob[arg]['win'][f"{key}_list"].append(n)
                else:
                    prob[arg]['lose_times'] += 1
                    if streak <= 0:
                        prob[arg]['streak'] -= 1
                    else:
                        if streak > prob[arg]['best']:
                            prob[arg]['best'] = streak
                        prob[arg]['streak'] = -1
                    prob[arg]['streak'] = prob[arg]['streak'] - 1
                    for key in keys_to_save:
                        if key in init:
                            n = Dc(str(init[key]).strip('\t').strip(')'))
                            prob[arg]['lose'][key] += n
                            prob[arg]['lose'][f"{key}_list"].append(n)
    key = f"{t1}-{t2}-{a1}-{a2}-{c1}-{c2}-{s1}-{s2}"
    p=prob[arg]
    wins = p['win_times']
    loses = p['lose_times']
    sample = wins + loses
    try:
        rate = wins / sample
        odd = 1 / rate
        rate2 = 1 - rate
        odd2 = 1 / rate2
        print("{}\n\n{}\nAmostra: {} | Wins: {} | Loses: {}\n\
        Win Rate: {:.2%} | Win Odd: {:.3}\n\
        Lose Rate: {:.2%} | Lose Odd: {:.3}\n\
        Streak: {} | Best: {} | Worst: {}\n".format(key,
            arg,
            sample,
            wins,
            loses,
            rate,
            odd,
            rate2,
            odd2,
            p['streak'],
            p['best'],
            p['worst']))

    except:
        rate = 0

    return rate, wins, loses, sample


if __name__ == '__main__':
    strategies_view()

