possible_errors = {'-', ' -', '- ', ' - ', ' ', ''}
not_conv = {'home_team', 'away_team', 'half_finished', 'handicap', 'league'}

def match_formatter(matches):

    formatted_list = []
    for match in matches:

        get_error = False
        current_status = match.find('td', class_='match_status').find('span').text

        if (current_status == ''):
            break

        match_id = match['data-match_id']
        league = match.find('td', class_='td_league').find('a').text
        home_team = match.find('td', class_='match_home').find('a').text
        away_team = match.find('td', class_='match_away').find('a').text
        score = match.find('td', class_='match_goal').text.split('-')
        handicap = match.find('td', class_='match_handicap').text.replace('\n', '').replace(' ', '').strip(')').split('(')
        if len(handicap) == 2:
            for n in range(2):
                handicap[n] = '0.0' if handicap[n] == '' else handicap[n]
        else:
            handicap.append('0.0')
        corners = match.find('td', class_='match_corner').find('div').find('span', class_='span_match_corner').text.split('-')

        attacks = match.find('td', class_='match_attach').find('div', class_='match_dangerous_attacks_div').text.split('-')
        shots = match.find('td', class_='match_shoot').find('div', class_='match_shoot_div').text.split('-')

        match = {
            'match_id': match_id,
            'league': league,
            'home_team': home_team,
            'away_team': away_team,
            'handicap': handicap,
            'home_score': score[0],
            'away_score': score[1],
            'home_corner': corners[0],
            'away_corner': corners[1],
            'home_attack': attacks[0],
            'away_attack': attacks[1],
            'home_shot': shots[0],
            'away_shot': shots[1],
            'current_minutes': current_status,
            'half_finished': False,
            'attacks': 0,
            'corners': 0,
            'shots': 0,
        }

        for key in match:
            if key != 'handicap':
                if match[key] in possible_errors:
                    get_error = True
        if get_error:
            continue

        if match['current_minutes'] == "Half":
            match['current_minutes'] = 45
            match['half_finished'] = True
        elif match['current_minutes'] == "Full":
            match['current_minutes'] = 90
            match['half_finished'] = True
        else:
            match['half_finished'] = False

        for key in match:
            if key not in not_conv:
                match[key] = int(match[key])

        match['attacks'] = match['home_attack'] + match['away_attack']
        match['corners'] = match['home_corner'] + match['away_corner']
        match['shots'] = match['home_shot'] + match['away_shot']
        formatted_list.append(match)

    return formatted_list