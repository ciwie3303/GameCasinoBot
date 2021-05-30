from time import sleep
from telethon import TelegramClient
import asyncio

from telethon import TelegramClient, events
from telethon.tl.types import PeerUser, MessageMediaDocument, PeerChannel, MessageMediaPhoto

from data.functions.db import update_balance

api_id = 3079664
api_hash = 'a0f7520299c0375f5ee2aad48cc3fec3'

client = TelegramClient('hi', api_id, api_hash, device_model="Iphone", system_version="6.12.0",
                        app_version="10 P (28)")

client.start()

async def checked_btc(user_id, cheque):

	await client.send_message('me', 'start')

	await client.send_message('BTC_CHANGE_BOT', '/start ' + cheque)
	await asyncio.sleep(0.2)

	transaction = await client.get_messages('BTC_CHANGE_BOT', limit=1)
	msg_transaction = transaction[0].message
	if 'Вы получили' in msg_transaction:
		msg_transaction = msg_transaction.replace('(', '').replace(')', '').split(' ')
		if msg_transaction[5] != 'RUB':
			print('Валюта была не в рублях!')

			return 'Валюта была не в рублях'
		else:
			amount = round(float(msg_transaction[4]))
			update_balance(user_id, amount)
			return f'Ваш чек проверен, на ваш счёт зачислено +{amount} RUB'

		await client.disconnect()

	elif 'Это телеграм бот криптоплатформы' in msg_transaction:
		return 'Ошибка при обналичивании чека'

		await client.disconnect()
	else:
		return msg_transaction
		
		await client.disconnect()
