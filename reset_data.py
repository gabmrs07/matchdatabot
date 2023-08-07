from db import DropBox


args = [('19', '30'), ('34', '45'), ('39', '45'), ('59', '70'), ('69', '80')]
dbox = DropBox('pHpPgE8H-T8AAAAAAAAAASLRzBIjEtV0_FBWgxsxL87389YY9e4ZpOJKeBH1OXav')
#matches = {}
#strategies = {}
strategies = dbox.download('strategies.json', '/corner')

for k in strategies.keys():
    print(k, strategies[k]['bank'], len(strategies[k]['match_ids']))

strategies["UNDER-39-45-20-0-3-5-WIN/DRAW"] = {'match_ids': [], 'bank': 100}

#dbox.upload('matches.json', matches, '/corner', mode='overwrite')
#dbox.upload('strategies.json', strategies, '/corner', mode='overwrite')