from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import  Bot, Dispatcher, executor, types

from datetime import datetime, timedelta
from glQiwiApi import QiwiWallet, QiwiWrapper

import logging, sqlite3, random, asyncio

admin = #admin
logging.basicConfig(level = logging.INFO)

bot = Bot(token = 'token', parse_mode='Markdown')
storage = MemoryStorage()

@dp.callback_query_handler(lambda c: c.data == 'buy')
async def buy(c: types.CallbackQuery):
	cena = 49
	msg = c.message
	code = random.randint(100, 999)

	async with QiwiWrapper(secret_p2p = qiwi) as w:
		code = random.randint(100, 999)
		bill = await w.create_p2p_bill(
			amount = cena,
			comment = f'Purchase on {cena}в‚Ѕ\nCode - {code}',
			life_time = datetime.now() + timedelta(minutes = 10))

		btn1 = InlineKeyboardButton(f'Pay {cena}в‚Ѕ', url = bill.pay_url)
		markup = InlineKeyboardMarkup().add(btn1)

		a = await msg.answer(f'The invoice has been issued, you have 10 minutes to purchase it!', reply_markup=markup)
		seconds = 600
		repeats = [1 for i in range(0, seconds)]
		for i in repeats:
			check = await w.check_p2p_bill_status(bill_id = bill.id)
			await asyncio.sleep(5)
			check = 'EXPIRED'
			if check == "PAID":
				await bot.send_message(admin, f'Topped up balance {cena}\nCode-{code}')
				await msg.answer('Successfully')

				chat_id = #CHANNEL ID
    			expire_date = datetime.now() + timedelta(days=1) #link duration
				link = await bot.create_chat_invite_link(chat_id, expire_date.timestamp, 1)

				break
			if check == 'EXPIRED':
				await a.edit_text("You didn't have time((")
				break
            
			await asyncio.sleep(10)

@dp.message_handler(commands=['start'])
async def start(msg: types.Message):
	btn1 = InlineKeyboardButton('Buy', callback_data='buy')
	markup = InlineKeyboardMarkup().add(btn1)

	await msg.reply('You need to pay to join the channel 49Р ', reply_markup=markup)

if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)
