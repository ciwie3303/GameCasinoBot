import sqlite3
import datetime
import time


def get_now_date():
    date = datetime.datetime.today().strftime("%d.%m.%Y")
    return date


def add_user_to_db(user_id):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    user = [user_id, 0, "False", "False", get_now_date()]
    cursor.execute(f'''INSERT INTO users(user_id, balance, twist, banned, registration_date) VALUES(?,?,?,?,?)''', user)
    db.commit()


def get_user(user_id):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f"""SELECT * FROM users WHERE user_id = '{user_id}'""")
    row = cursor.fetchone()
    return row


def get_all_users():
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f"""SELECT * FROM users""")
    row = cursor.fetchall()
    return row


def get_all_games():
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f'''SELECT * FROM games_logs''')
    row = cursor.fetchall()
    return row


def get_all_slots_games():
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f'''SELECT * FROM slots_logs''')
    row = cursor.fetchall()
    return row


def get_all_bets_sum():
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f'''SELECT SUM(bank) FROM games_logs''')
    row = cursor.fetchone()[0]
    return row


def get_all_slots_bets_sum():
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f'''SELECT SUM(bet) FROM slots_logs''')
    row = cursor.fetchone()[0]
    return row


def get_all_today_users():
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f"""SELECT * FROM users WHERE registration_date = '{get_now_date()}' """)
    row = cursor.fetchone()
    return row


def get_all_today_games():
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f'''SELECT * FROM games_logs WHERE date = '{get_now_date()}' ''')
    row = cursor.fetchall()
    return row


def get_all_today_slots_games():
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f'''SELECT * FROM slots_logs WHERE date = '{get_now_date()}' ''')
    row = cursor.fetchall()
    return row


def get_all_today_bets_sum():
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f'''SELECT SUM(bank) FROM games_logs WHERE date = '{get_now_date()}' ''')
    row = cursor.fetchone()[0]
    return row


def get_all_today_slots_bets_sum():
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f'''SELECT SUM(bet) FROM slots_logs WHERE date = '{get_now_date()}' ''')
    row = cursor.fetchone()[0]
    return row


def change_spinup_status(user_id, status):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f"""UPDATE users SET twist = '{status}' WHERE user_id = '{user_id}' """)
    db.commit()


def update_balance(user_id, amount, add=True):
    if add:
        balance = get_user(user_id)[1] + amount
    else:
        balance = amount
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f"""UPDATE users SET balance = '{balance}' WHERE user_id = '{user_id}' """)
    db.commit()


def add_other_game_to_db(game_id, player_1, bet, game_name):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    game = [game_id, player_1, bet, game_name]
    cursor.execute(f'''INSERT INTO other_games(game_id, player_1, bet, game_name) VALUES(?,?,?,?)''', game)
    db.commit()


def get_other_games():
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f"""SELECT * FROM other_games""")
    row = cursor.fetchall()
    return row


def get_other_game(game_id):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f"""SELECT * FROM other_games WHERE game_id = '{game_id}'""")
    row = cursor.fetchone()
    return row


def delete_other_game(game_id):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f"""DELETE FROM other_games WHERE game_id = '{game_id}'""")
    db.commit()


def add_blackjack_game_to_db(game_id, player_1, bet):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    game = [game_id, player_1, 0, 0, 0, 0, 0, 0, 0, bet, "False"]
    cursor.execute(f'''INSERT INTO blackjack_games VALUES(?,?,?,?,?,?,?,?,?,?,?)''', game)
    db.commit()


def get_blackjack_games():
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f"""SELECT * FROM blackjack_games WHERE status = 'False' """)
    row = cursor.fetchall()
    return row


def get_blackjack_game(game_id):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f"""SELECT * FROM blackjack_games WHERE game_id = '{game_id}'""")
    row = cursor.fetchone()
    return row


def update_player_blackjack(game_id, player_2):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f"""UPDATE blackjack_games SET player_2 = '{player_2}' WHERE game_id = '{game_id}' """)
    db.commit()

def update_blackjack_game_status(game_id):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f"""UPDATE blackjack_games SET status = 'True' WHERE game_id = '{game_id}' """)
    db.commit()


def add_card_to_player(game_id, player, number):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f"""UPDATE blackjack_games SET {player}_amount = {player}_amount + 1 WHERE game_id = '{game_id}' """)
    db.commit()
    cursor.execute(f"""UPDATE blackjack_games SET {player}_result = {player}_result + {number} WHERE game_id = '{game_id}' """)
    db.commit()


def delete_blackjack_game(game_id):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f"""DELETE FROM blackjack_games WHERE game_id = '{game_id}'""")
    db.commit()


def add_game_log(game_id, winner, loser, bank, profit, game_name):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    game = [game_id, winner, loser, bank, profit, game_name, get_now_date()]
    cursor.execute(f'''INSERT INTO games_logs VALUES(?,?,?,?,?,?,?)''', game)
    db.commit()


def add_slots_log(player, bet, win, win_amount):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    game = [player, bet, win, win_amount, get_now_date()]
    cursor.execute(f'''INSERT INTO slots_logs VALUES(?,?,?,?,?)''', game)
    db.commit()


def add_jackpot_log(winner, bank, profit, losers):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    game = [winner, bank, profit, losers, get_now_date()]
    cursor.execute(f'''INSERT INTO jackpot_logs VALUES(?,?,?,?,?)''', game)
    db.commit()


def get_user_other_game_win_sum(user_id):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f'''SELECT SUM(bank - profit) FROM games_logs WHERE winner = '{user_id}'
    AND NOT game_name = 'blackjack'
    AND NOT game_name = 'bakkara' ''')
    row = cursor.fetchone()[0]
    return row


def get_user_other_game_lose_sum(user_id):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f'''SELECT SUM((bank - profit)/2) FROM games_logs WHERE loser = '{user_id}'
    AND NOT game_name = 'blackjack'
    AND NOT game_name = 'bakkara' ''')
    row = cursor.fetchone()[0]
    return row


def get_user_other_game_win_amount(user_id):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f'''SELECT COUNT(winner) FROM games_logs WHERE winner = '{user_id}'
    AND NOT game_name = 'blackjack'
    AND NOT game_name = 'bakkara' ''')
    row = cursor.fetchone()[0]
    return row


def get_user_other_lose_amount(user_id):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f'''SELECT COUNT(loser) FROM games_logs WHERE loser = '{user_id}' 
    AND NOT game_name = 'blackjack'
    AND NOT game_name = 'bakkara' ''')
    row = cursor.fetchone()[0]
    return row


def get_user_blackjack_game_win_amount(user_id):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f'''SELECT COUNT(winner) FROM games_logs WHERE winner = '{user_id}'
    AND game_name = 'blackjack' ''')
    row = cursor.fetchone()[0]
    return row


def get_user_blackjack_lose_amount(user_id):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f'''SELECT COUNT(loser) FROM games_logs WHERE loser = '{user_id}' 
    AND game_name = 'blackjack' ''')
    row = cursor.fetchone()[0]
    return row


def get_user_blackjack_game_win_sum(user_id):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f'''SELECT SUM(bank - profit) FROM games_logs WHERE winner = '{user_id}'
    AND game_name = 'blackjack' ''')
    row = cursor.fetchone()[0]
    return row


def get_user_blackjack_game_lose_sum(user_id):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f'''SELECT SUM((bank - profit)/2) FROM games_logs WHERE loser = '{user_id}'
    AND game_name = 'blackjack' ''')
    row = cursor.fetchone()[0]
    return row


def add_bakkara_game_to_db(game_id, player_1, bet):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    game = [game_id, player_1, 0, 0, 0, None, None, bet, "False"]
    cursor.execute(f'''INSERT INTO bakkara_games VALUES(?,?,?,?,?,?,?,?,?)''', game)
    db.commit()


def update_bakkara_game_status(game_id):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f"""UPDATE bakkara_games SET status = 'True' WHERE game_id = '{game_id}' """)
    db.commit()


def update_player_bakkara(game_id, player_2):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f"""UPDATE bakkara_games SET player_2 = '{player_2}' WHERE game_id = '{game_id}' """)
    db.commit()


def get_bakkara_game(game_id):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f"""SELECT * FROM bakkara_games WHERE game_id = '{game_id}'""")
    row = cursor.fetchone()
    return row


def get_bakkara_games():
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f"""SELECT * FROM bakkara_games WHERE status = 'False' """)
    row = cursor.fetchall()
    return row


def add_card_to_bakkara_player(game_id, player, number):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f"""UPDATE bakkara_games SET {player}_result = '{number}' WHERE game_id = '{game_id}' """)
    db.commit()


def add_cards_to_bakkara_player(game_id, player, cards):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f"""UPDATE bakkara_games SET {player}_cards = '{cards}' WHERE game_id = '{game_id}' """)
    db.commit()

def delete_bakkara_game(game_id):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f"""DELETE FROM bakkara_games WHERE game_id = '{game_id}'""")
    db.commit()

def get_user_bakkara_game_win_amount(user_id):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f'''SELECT COUNT(winner) FROM games_logs WHERE winner = '{user_id}'
    AND game_name = 'bakkara' ''')
    row = cursor.fetchone()[0]
    return row


def get_user_bakkara_lose_amount(user_id):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f'''SELECT COUNT(loser) FROM games_logs WHERE loser = '{user_id}' 
    AND game_name = 'bakkara' ''')
    row = cursor.fetchone()[0]
    return row


def get_user_bakkara_game_win_sum(user_id):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f'''SELECT SUM(bank - profit) FROM games_logs WHERE winner = '{user_id}'
    AND game_name = 'bakkara' ''')
    row = cursor.fetchone()[0]
    return row


def get_user_bakkara_game_lose_sum(user_id):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f'''SELECT SUM((bank - profit)/2) FROM games_logs WHERE loser = '{user_id}'
    AND game_name = 'bakkara' ''')
    row = cursor.fetchone()[0]
    return row


def add_jackpot_bet(user_id, bet):
    if get_jackpot_bet(user_id) == None:
        if len(get_jackpot_bets()) == 1:
            update_jackpot_end_time(time.time() + 120)
        db = sqlite3.connect('data/database.db')
        cursor = db.cursor()
        bet = [user_id, bet]
        cursor.execute(f'''INSERT INTO jackpot_bets VALUES(?,?)''', bet)
        db.commit()
    else:
        db = sqlite3.connect('data/database.db')
        cursor = db.cursor()
        cursor.execute(f'''UPDATE jackpot_bets SET bet = bet + '{bet}' WHERE user_id = '{user_id}' ''')
        db.commit()


def get_jackpot_end_time():
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f"""SELECT * FROM jackpot_game """)
    row = cursor.fetchone()[0]
    return row


def update_jackpot_end_time(end_time):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f'''UPDATE jackpot_game SET end_time = '{end_time}' ''')
    db.commit()

def get_jackpot_bets():
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f"""SELECT * FROM jackpot_bets """)
    row = cursor.fetchall()
    return row


def get_jackpot_bet(user_id):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f"""SELECT * FROM jackpot_bets WHERE user_id = '{user_id}' """)
    row = cursor.fetchone()
    return row


def get_jackpot_bets_amount():
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f'''SELECT SUM(bet) FROM jackpot_bets ''')
    row = cursor.fetchone()[0]
    return row


def delete_jackpot_bets():
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f'''DELETE FROM jackpot_bets''')
    db.commit()


def get_user_jackpot_win_amount(user_id):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f'''SELECT COUNT(winner) FROM jackpot_logs WHERE winner = '{user_id}' ''')
    row = cursor.fetchone()[0]
    return row



def get_user_jackpot_win_sum(user_id):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f'''SELECT SUM(bank - profit) FROM jackpot_logs WHERE winner = '{user_id}' ''')
    row = cursor.fetchone()[0]
    return row


def get_user_slots_game_amount(user_id):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f'''SELECT COUNT(player) FROM slots_logs WHERE player = '{user_id}' ''')
    row = cursor.fetchone()[0]
    return row


def get_user_slots_game_bet_amount(user_id):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f'''SELECT SUM(bet) FROM slots_logs WHERE player = '{user_id}' ''')
    row = cursor.fetchone()[0]
    return row


def get_user_slots_win_sum(user_id):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f'''SELECT SUM(win_amount) FROM slots_logs WHERE player = '{user_id}' ''')
    row = cursor.fetchone()[0]
    return row


def get_user_slots_lose_sum(user_id):
    db = sqlite3.connect('data/database.db')
    cursor = db.cursor()
    cursor.execute(f'''SELECT SUM(win_amount) FROM slots_logs WHERE player = '{user_id}' AND win_amount = 0 ''')
    row = cursor.fetchone()[0]
    return row

