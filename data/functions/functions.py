from PIL import Image, ImageDraw, ImageFont
import string
import random
import os
import time
import asyncio
from config import config
from data.functions.db import get_jackpot_bets, delete_jackpot_bets, get_jackpot_bets_amount, update_balance, \
    get_jackpot_end_time, add_jackpot_log

now_time = time.time()

def get_first_bakkara_screen(watermark, game_id, player):
    cord = [(15, 75)]
    im = Image.open("background_2.jpg")
    watermark = Image.open(f"data/photos/{watermark}").convert("RGBA")
    im.paste(watermark, cord[0], watermark)
    font = ImageFont.truetype('font.ttf', size=16)
    draw_text = ImageDraw.Draw(im)
    draw_text.text(
        (635, 80),
        'Информация:\n'
        f'Game ID: {game_id}\n'
        f'Player: {player}\n',
        font=font,
        fill=('#FFFFFF')
    )
    im.save(f"{game_id}_{player}.jpg")


def add_bakkara_card(watermark, game_id, player, cards):
    cord = [(225, 75), (435, 75)]
    im = Image.open(f"{game_id}_{player}.jpg")
    watermark = Image.open(f"data/photos/{watermark}").convert("RGBA")
    im.paste(watermark, cord[len(cards.split(":"))-2], watermark)
    im.save(f"{game_id}_{player}.jpg")


def get_bakkara_result(game_id, player_1, player_2, bet, p1_cards, p2_cards, winner, p1_result, p2_result):
    p1_cord = [(15, 45), (225, 45), (435, 45)]
    p2_cord = [(15, 405), (225, 405), (435, 405)]
    if winner == 0:
        winner = "НИЧЬЯ"
    im = Image.open('back.jpg')
    for i in range(0, len(p1_cards.split(":"))):
        card = p1_cards.split(":")[i]
        watermark = Image.open(f'data/photos/{card}').convert("RGBA")
        im.paste(watermark, p1_cord[i], watermark)
    for i in range(0, len(p2_cards.split(":"))):
        card = p2_cards.split(":")[i]
        watermark_2 = Image.open(f'data/photos/{card}').convert("RGBA")
        im.paste(watermark_2, p2_cord[i], watermark_2)
    font = ImageFont.truetype('font.ttf', size=22)
    font_2 = ImageFont.truetype('font.ttf', size=50)
    draw_text = ImageDraw.Draw(im)
    draw_text.text(
        (280, 320),
        'VS',
        font=font_2,
        fill=('#FFFFFF'))
    draw_text.text(
        (620, 295),
        f'Game ID: {game_id}\n'
        f'Ставка: {bet}\n'
        f'Победитель: {winner}\n',
        font=font,
        fill=('#FFFFFF'))
    draw_text.text(
        (630, 50),
        f'User ID: {player_1}\n'
        f'Очков: {p1_result}\n',
        font=font,
        fill=('#FFFFFF'))

    draw_text.text(
        (630, 570),
        f'User ID: {player_2}\n'
        f'Очков: {p2_result}\n',
        font=font,
        fill=('#FFFFFF'))

    im.save(f"result_{game_id}.jpg")

def gen_random_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    rand_string = ''.join(random.sample(letters_and_digits, length))

    return rand_string


def delete_game_photos(game_id, player_1, player_2):
    os.remove(f"{game_id}_{player_1}.jpg")
    os.remove(f"{game_id}_{player_2}.jpg")
    os.remove(f"result_{game_id}.jpg")


async def game_time(bot):
    while True:
        await asyncio.sleep(2)
        now_time = time.time()
        if get_jackpot_end_time() < now_time:
            losers_list = []
            text, check, win_amount, winner_id = await get_jackpot_result(bot)
            if check:
                bank = get_jackpot_bets_amount()
                update_balance(winner_id, win_amount)
                bets = get_jackpot_bets()
                profit = bank - win_amount
                for bet in bets:
                    if bet[0] != winner_id:
                        losers_list.append(str(bet[0]))
                        await bot.send_message(chat_id=bet[0], text=text)

                    else:
                        await bot.send_message(chat_id=winner_id,
                                               text="Поздравляем с победой в джекпоте!\n\n"
                                                      f"<b>{win_amount}</b> RUB зачислены на ваш баланс.")
                losers = ":".join(losers_list)
                add_jackpot_log(winner_id, bank, profit, losers)
                delete_jackpot_bets()
            else:
                pass


async def get_jackpot_result(bot):
    bets = get_jackpot_bets()
    if len(bets) >= 2:
        bets_sum = get_jackpot_bets_amount()
        win_number = random.randint(1, 999999)
        win_amount = (bets_sum - bets_sum / 100 * float(config('game_percent')))
        last_number = 0
        for bet in bets:
            percent = int(round(bet[1] / (bets_sum / 100)))
            number = int(999999 / 100 * percent + last_number)
            if win_number in range(last_number, number):
                winner_id = bet[0]
                winner_percent = percent
            last_number = number
        user = await bot.get_chat(winner_id)
        text = f"Победу в джекпоте с процентом {winner_percent} одержал <a href='t.me//{user.username}'>{user.first_name}</a> забрав {win_amount} RUB"
        return text, True, win_amount, winner_id
    else:
        return 0, False, 0, 0
