from random import randint

def handicap_solver(s1, s2, h1):
    if h1 != 0:
        fav = 'home' if h1 < 0 else 'away'
        diff = s1 - s2
        if diff in {1, -1}:
            winner = 'home' if diff == 1 else 'away'
            fav_losing = (fav != winner)
            print(f"HomeTeam {s1} x {s2} AwayTeam | Hand: {h1} | Fav: {fav_losing}")
        else:
            print('Diferença maior que 1 gol!')
    else:
        print('Jogo empatado!')

if __name__ == '__main__':
    handicaps = [-2, -1.5, -1, -0.75, -0.5, -0.25, 0.0, 0.25, 0.5, 0.75, 1, 1.5, 2]
    for n in range(100):
        handicap_solver(randint(0, 5), randint(0, 5), handicaps[randint(0, 12)])
