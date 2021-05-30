import configparser
import os
import time

path = 'data/config.cfg'
games_photo = "https://i.imgur.com/UyyQ0Tu.jpg"
cabinet_photo = "https://i.imgur.com/3X4LsUl.jpg"
slots_photo = "https://i.imgur.com/Q7cUdjb.jpg"
other_games_photo ="https://i.imgur.com/tcbYMfy.jpg"
blackjack_photo = "https://i.imgur.com/gxEbB4I.jpg"
bakkara_photo = "https://i.imgur.com/6FuKbx1.jpg"
jackpot_photo = "https://i.imgur.com/ixsHnKJ.jpg"

link_regex = "^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$"

other_games_info = {"dice": {"emoji": "🎲", "text": "🎲Кости"},
                    "darts": {"emoji": "🎯", "text": "🎯Дартс"},
                    "basketball": {"emoji": "🏀", "text": "🏀Баскетбол"},
                    "bowling": {"emoji": "🎳", "text": "🎳Боулинг"}}

slots_values = {
    "2_same" : [32, 6, 62, 4, 2, 49, 59, 48, 63, 44, 38,
                21, 32, 16, 3, 23, 44, 54, 27, 33, 42, 11,
                41, 13, 24, 17 ],
    "3_same" : [43, 11, 22]
}

bakkara_values = {
    "1" : {"value" : 1, "name": 1, "file_name" : "1h.png:1d.png:1c.png:1s.png"},
    "2" : {"value" : 2, "name": 2, "file_name" : "2h.png:2d.png:2c.png:2s.png"},
    "3" : {"value" : 3, "name": 3, "file_name" : "3h.png:3d.png:3c.png:3s.png"},
    "4" : {"value" : 4, "name": 4, "file_name" : "4h.png:4d.png:4c.png:4s.png"},
    "5" : {"value" : 5, "name": 5, "file_name" : "5h.png:5d.png:5c.png:5s.png"},
    "6" : {"value" : 6, "name": 6, "file_name" : "6h.png:6d.png:6c.png:6s.png"},
    "7" : {"value" : 7, "name": 7, "file_name" : "7h.png:7d.png:7c.png:7s.png"},
    "8" : {"value" : 8, "name": 8, "file_name" : "8h.png:8d.png:8c.png:8s.png"},
    "9" : {"value" : 9, "name": 9, "file_name" : "9h.png:9d.png:9c.png:9s.png"},
    "10" : {"value" : 10, "name": 10, "file_name" : "10h.png:10d.png:10c.png:10s.png"},
    "jack" : {"value" : 10, "name": 1, "file_name" : "11h.png:11d.png:11c.png:11s.png"},
    "lady" : {"value" : 10, "name": 1, "file_name" : "12h.png:12d.png:12c.png:12s.png"},
    "king" : {"value" : 10, "name": 1, "file_name" : "13h.png:13d.png:13c.png:13s.png"},


}

def create_config():
    config = configparser.ConfigParser()
    config.add_section("Settings")
    config.set("Settings", "bot_token", "token")
    config.set("Settings", "admin_id", "123123:1123211")
    config.set("Settings", "p2p_qiwi_key", "0")
    config.set("Settings", "admin_chat", "-100")
    config.set("Settings", "game_percent", "20")
    config.set("Settings", "ref_percent", "5")

    with open(path, "w") as config_file:
        config.write(config_file)


def check_config_file():
    if not os.path.exists(path):
        create_config()

        print('Config created')
        time.sleep(3)
        exit(0)


def config(what):
    config = configparser.ConfigParser()
    config.read(path)

    value = config.get("Settings", what)

    return value


def edit_config(setting, value):
    config = configparser.ConfigParser()
    config.read(path)

    config.set("Settings", setting, value)

    with open(path, "w") as config_file:
        config.write(config_file)


check_config_file()
