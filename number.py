import sqlite3
import json

DATABASE_PATH = 'smashdata/ultimate_player_database/ultimate_player_database.db'

P_ID = 0
P_SCORE = 2

def get_player_name(db, player_id):
    cur = db.cursor()

    cur.execute('select tag from players where player_id = ?', (player_id, ))

    row = cur.fetchone()

    cur.close()

    return row[0]


def get_wins(db, from_id, use_online):
    print('getting wins for player {} (id {})'.format(get_player_name(db, from_id), from_id))

    set_cursor = db.cursor()

    set_cursor.execute('select winner_id, p1_id, p2_id, p1_score, p2_score, tournament_key from sets where winner_id = ?', (from_id, ))

    wins = []
    found_ids = set()

    for row in set_cursor:
        loser_num = 1 if from_id == row[2] else 2

        if row[P_ID + loser_num] in found_ids:
            continue
        if row[P_SCORE + loser_num] == -1:
            continue

        tournament_info_cursor = db.cursor()

        tournament_info_cursor.execute('select online, cleaned_name from tournament_info where key = ?', (row[5], ))
        tournament_row = tournament_info_cursor.fetchone()
        if tournament_row[0] == 1:
            continue

        wins.append((row[P_ID + loser_num], tournament_row[1]))
        found_ids.add(row[P_ID + loser_num])

        tournament_info_cursor.close()

    set_cursor.close()

    return wins


def get_wins_multiple_ids(db, ids, use_online):
    set_cursor = db.cursor()

    wildcard_string = '?,' * len(ids)
    wildcard_string = wildcard_string[:-1]

    set_cursor.execute('select winner_id, p1_id, p2_id, p1_score, p2_score, tournament_key from sets where winner_id in (' + wildcard_string + ')', tuple(ids))

    wins = []
    found_ids = set()

    for row in set_cursor:
        loser_num = 1 if row[0] == row[2] else 2
        winner_num = 3 - loser_num

        if row[P_ID + loser_num] in found_ids:
            continue
        if row[P_SCORE + loser_num] == -1:
            continue

        tournament_info_cursor = db.cursor()

        tournament_info_cursor.execute('select online, cleaned_name from tournament_info where key = ?', (row[5], ))
        tournament_row = tournament_info_cursor.fetchone()
        if tournament_row[0] == 1:
            continue

        wins.append((row[P_ID + winner_num], row[P_ID + loser_num], tournament_row[1]))
        found_ids.add(row[P_ID + loser_num])

        tournament_info_cursor.close()

    set_cursor.close()

    return wins


def print_path(db, first_id, last_id, progressions):
    path = []

    cur_id = last_id
    while cur_id != first_id:
        progression = progressions[cur_id]
        path.append((cur_id, progression[1]))
        cur_id = progression[0]

    print('{} has a {} number of {}'.format(get_player_name(db, first_id), get_player_name(db, last_id), len(path)))
    print(get_player_name(db, first_id))

    for path_element in reversed(path):
        print('-> {} (@ {})'.format(get_player_name(db, path_element[0]), path_element[1]))


def find_number(db, from_id, to_id, use_online):
    progressions = {}

    progressions[from_id] = ()

    id_list = []

    id_list.append(from_id)
    idx = 0

    iteration = 1

    while True:
        ids = id_list[idx:]

        idx = len(id_list)

        print('phase {}: getting wins for {} players'.format(iteration, len(ids)))
        for win in get_wins_multiple_ids(db, ids, use_online):
            if win[1] in progressions.keys():
                continue
            id_list.append(win[1])
            progressions[win[1]] = (win[0], win[2])

            if win[1] == to_id:
                print_path(db, from_id, to_id, progressions)
                return
        iteration += 1

def main():
    db = sqlite3.connect(DATABASE_PATH)

    from_id = input('input beginning id: ')
    to_id = input('input end id: ')
    use_online = input('use online? (y/n) ').upper() == 'Y'

    print('Finding path from player {} to player {}'.format(get_player_name(db, from_id), get_player_name(db, to_id)))

    find_number(db, from_id, to_id, use_online)

    db.close() 

if __name__ == '__main__':
    main()