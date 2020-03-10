"""
Telegram 8M Bot v0.1
"""

import logging
import json
from aiogram import Bot, Dispatcher, executor, types

"""
ENTER YOUR API_TOKEN HERE v v v v v v v v 
"""
API_TOKEN = ''
ADMIN_ID = 0
"""
ENTER YOUR API_TOKEN HERE ^ ^ ^ ^ ^ ^ ^ ^ 
                          EXAMPLE:   API_TOKEN = "111111111:AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
                                     ADMIN_ID = 15347332
"""
if not API_TOKEN or not ADMIN_ID:
    print("ENTER API_TOKEN (line 12) and ADMIN_ID (line 13)")
    quit()


logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# JSON FILES IMPORT
json_file = open('pay_dic.json', 'r', encoding="utf8")
pay_dic = json.load(json_file)

# length of list
toplen = 100

emoji_list1 = [' 💎🥇 ', ' 🔥🥈 ', ' 👑🥉 ', ' 💰 ', ' 🚀 '] + ['        '*toplen]
emoji_list2 = ['  🥇💎 ', ' 🥈🔥 ', ' 🥉👑 ', ' 💰 ', ' 🚀 '] + ['        '*toplen]



# Save gay-rate
def save_rate():
    json.dump(pay_dic, open('pay_dic.json', 'w'))


# Authorization decorator
def admin(func):
    async def firewall(message):
        if message['from']['id'] != ADMIN_ID:
            return await message.reply("Access Denied", reply=False)
        return await func(message)

    return firewall


# /start and /help echos
@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Hi! I'm 8M Bot. That’s what I can do.:\n"
                        "/top - Show top donations\n"
                        "/sc - Rank list\n"
                        "/add - add new donation (admin only)\n"
                        "/list - Users list (admin only)")

# Rank list - /sc
@dp.message_handler(commands=['sc'])
async def script(message: types.Message):
    await message.answer("""
        Rank list:

 💎 - Illuminati of the Order 
 🔥 - Overmind
 👑 - The King
 💰 - Richer
 🚀 - Hero
 🎗 - VIP
 
 💩 - Ass
                                    """)

# Show Top - /top
@dp.message_handler(commands=['top'])
async def top(message: types.Message):
    _result = ''
    r = 1
    _sum = 0

    pay_list = list(pay_dic.values())
    pay_list.sort(key=lambda x: int(x[1]), reverse=True)

    for p in pay_list:
        try:
            emoji1 = '💩' if int(p[1]) == 0 else emoji_list1[r - 1] if r < 6 else ' 🎗 ' if int(p[1]) > 200 else emoji_list1[r - 1]
            emoji2 = emoji_list2[r - 1] if p[1] != '0' else ''
            _result += f"{emoji1} {p[0]} :  {p[1]} RUB {emoji2 if r < 4 else ''}\n"
            r += 1

            _sum += int(p[1])

            if r == 4:
                _result += '\n'

        except KeyError:
            pass

    # Info Message
    await message.reply(f" —   —   —   — TOP DONATIONS —   —   —   —   —\n\n"
                        f"{_result}"
                        f"—   —   —   —   —   —   —   —   —   —   —   —   —\n"
                        f"Total donation:  {_sum}/6000 RUB  {'⚠️' if _sum < 6000 else '✅'}"
                        )

# Add donation - /add ID VAL
@dp.message_handler(commands=['add'])
@admin
async def add_pay(message: types.Message):

    try:

        msg = message.text.lower().strip(""",./!';[]{}-=\+|()"'""").split(' ')

        tar_id = msg[1]
        money = int(msg[2])
        person = pay_dic.get(tar_id)[0]

        temp = {tar_id:
                    [person, str(
                        int(pay_dic.get(tar_id)[1]) + money
                    )
                     ]
                }
        pay_dic.update(temp)

        # Info Message
        await message.reply(f"❤️ {pay_dic.get(tar_id)[0]} DONATED {money} RUBLES! ❤️", reply=False)

    except:
        await message.reply(f"Error [03]", reply=True)

    save_rate()

# List of users - /list
@dp.message_handler(commands=['list'])
@admin
async def list_of_users(message: types.Message):

    # Info Message
    pay_list = list(pay_dic.items())
    pay_list.sort(key=lambda x: int(x[0]), reverse=False)
    _result = 'id:  person\n'

    for i in pay_list:
        _result += f"{i[0]}: {i[1][0]} \n"

    await message.reply(_result, reply=True)


# Got any message script - 'optional-word'
@dp.message_handler()
async def main(message: types.Message):

    # MSG -> LIST of WORDS
    msg = message.text.lower().strip(""",./!';[]{}-=\+|()"'""").split(' ')

    optional = ['оплатил', 'скинул', 'прислал', 'перевёл', 'отправил', 'проверяй', 'пререкинул', 'проплатил', '+',
               'заплачен', 'оплачено', 'выслал', 'накинул', 'проплатил']

    # IF some G-word in message
    if [w for w in msg for o in optional if w == o]:
        await message.reply(f"YAY! You are an absolute star!", reply=True)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
