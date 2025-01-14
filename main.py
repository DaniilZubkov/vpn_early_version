import threading
import time
import datetime


from aiogram import Dispatcher, Bot, executor
from keyboards import main_keyboard, payment_keyboard1, profile_keyboard, payment_keyboard, pay_the_loot_keyboard, network1, succes_or_invalid
from aiogram.types import Message, CallbackQuery
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import asyncio
import requests
import os
import subprocess
from db import Database


bot = Bot('7934741203:AAHFESqtDITl5uXL3iLxztRCAomofQoW16Y')
dp = Dispatcher(bot)
proxy_host = '178.207.13.88'
proxy_port = '1080'
db = Database('database.db')

BOT_NICKNAME = 'pump_vpn_bot'
cost = ''
WALLET = ''
NETWORK = ''
user_count = ''
GROUP_CHAT_ID = -1002192140565
sum = ''

# YOUR HOSTS
free_hosts = {
    '🇩🇪 Germany': {
        'ip': '',
        'port': ''
    },
    '🇳🇱 Netherlands': {
        'ip': '',
        'port': ''
    },
    '🇫🇷 France': {
        'ip': '',
        'port': ''
    },
    '🇬🇧 England': {
        'ip': '',
        'port': ''
    },
    '🇵🇱 Poland': {
        'ip': '',
        'port': ''
    },
    '🇺🇸 USA': {
        'ip': '',
        'port': ''
    }
}


other_hosts = {
    # EUR
    '🇮🇹 Italy': {
        'ip': '',
        'port': ''
    },
    '🇧🇪 Belgium': {
        'ip': '',
        'port': ''
    },
    '🇨🇭 Switzerland': {
        'ip': '',
        'port': ''
    },
    '🇦🇹 Austria': {
        'ip': '',
        'port': ''
    },
    '🇸🇰 Slovakia': {
        'ip': '',
        'port': ''
    },
    '🇪🇸 Spain': {
        'ip': '',
        'port': ''
    },
    '🇵🇹 Portugal': {
        'ip': '',
        'port': ''
    },
    '🇨🇿 Czech Republic': {
        'ip': '',
        'port': ''
    },
    # ASIA
    '🇯🇵 Japan': {
        'ip': '',
        'port': ''
    },
    '🇸🇬 Singapore': {
        'ip': '',
        'port': ''
    },
    '🇲🇾 Malaysia': {
        'ip': '',
        'port': ''
    },
    '🇮🇩 Indonesia': {
        'ip': '',
        'port': ''
    },
    '🇹🇭 Thailand': {
        'ip': '',
        'port': ''
    },
    '🇻🇳 Vietnam': {
        'ip': '',
        'port': ''
    },
    '🇵🇭 Philippines': {
        'ip': '',
        'port': ''
    },
    '🇹🇷 Turkey': {
        'ip': '',
        'port': ''
    },
    '🇹🇲 Turkmenistan': {
        'ip': '',
        'port': ''
    },
    '🇰🇿 Kazakhstan': {
        'ip': '',
        'port': ''
    },
}

def days_to_seconds(days):
    return days * 24 * 60 * 60


def time_sub_day(get_time):
    time_now = int(time.time())
    middle_time = int(get_time) - time_now
    if middle_time <= 0:
        return False
    else:
        dt = str(datetime.timedelta(seconds=middle_time))
        dt = dt.replace("days", 'дней')
        return dt


def calculate_sum_from_rubs_to_dollars(num):
    return round(num / 90.00, 2)


@dp.message_handler(commands=['start'])
async def start(message: Message):
    await message.answer(f"🤖 Привет, {message.from_user.first_name}! Я Pump VPN - помогу тебе обойти блокировку различных источников, которые недоступны в РФ и не только.", reply_markup=main_keyboard)
    # Проверка подписки на старте и выдача пробного доступа

    if (not db.user_exists(message.from_user.id)):
        db.add_user(message.from_user.id)
        db.set_nickname(message.from_user.id, message.from_user.username)
        db.set_signup(message.from_user.id, 'done')
        user_id = message.from_user.id
        if db.get_sub_status(user_id):
            time_sub = int(time.time() + days_to_seconds(1)) - int(time.time())
            db.set_time_sub(user_id, time_sub)
            await message.answer(f'✅ Вам был выдан <b>пробный переод на 1 день</b>', parse_mode='html')
        else:
            time_sub = int(time.time() + days_to_seconds(1))
            db.set_time_sub(user_id, time_sub)
            await message.answer(f'✅ Вам был выдан <b>пробный период на 1 день</b>', parse_mode='html')
        start_command = message.text
        referrer_id = str(start_command[7:])
        if str(referrer_id) != "":
            if str(referrer_id) != str(message.from_user.id):
                db.add_user(message.from_user.id, referrer_id)
                db.set_nickname(message.from_user.id, message.from_user.username)
                db.set_signup(message.from_user.id, 'done')
                user_id = message.from_user.id
                if db.get_sub_status(user_id):
                    time_sub = int(time.time() + days_to_seconds(1)) - int(time.time())
                    db.set_time_sub(user_id, time_sub)
                    await message.answer(f'✅ Вам был выдан <b>пробный период на 1 день</b>', parse_mode='html')
                else:
                    time_sub = int(time.time() + days_to_seconds(1))
                    db.set_time_sub(user_id, time_sub)
                    await message.answer(f'✅ Вам был выдан <b>пробный период на 1 день</b>', parse_mode='html')
                try:
                    await bot.send_message(referrer_id,
                                           "✅ По вашей ссылке зарегистрировался новый пользователь.\n\n <b>Кошелек пополнен на 10₽</b>\n\n", parse_mode='html')
                    db.set_user_wallet_make(referrer_id, 10)
                    db.set_count_refers(referrer_id)
                    """
                    Можно добавить бонус на 10 дней доступа 
                    """
                    # if db.get_sub_status(referrer_id):
                    #     time_sub = int(time.time() + days_to_seconds(10)) - int(time.time())
                    #     db.set_time_sub(referrer_id, time_sub)
                    # else:
                    #     time_sub = int(time.time() + days_to_seconds(10))
                    #     db.set_time_sub(referrer_id, time_sub)
                except:
                    pass
            else:
                pass
        else:
            pass
    else:
        if db.get_sub_status(message.from_user.id):
            await message.answer('✅ Есть доступ к боту')
        else:
            await message.answer(
                f'🚨 Доступ закончился! {message.from_user.first_name}, нам нужно это исправить!\n\n'
                f'🌎 <b>Пользуйся всеми серверами и без переподключения при оплате доступа!</b>',
                reply_markup=payment_keyboard1, parse_mode='html')

@dp.message_handler(content_types=['text'])
async def loot_for_wallet(message: Message):
    global cost, user_count, sum
    if message.text.isdigit():
        sum = int(message.text)
        user_count = calculate_sum_from_rubs_to_dollars(sum)
        await message.answer(f'🤖 ***Переведите сумму ниже на адрес кошелька:***\n\n'
                             f'`{WALLET}`\n\n'
                             f'❗ ***Потом пришлите пришлите скриншот оплаты. В описании под скриншотом нужно вставить хэш транзакции, иначе бот не засчитает оплату. (сеть {NETWORK})***\n\n'
                             f'💵 К оплате: ***{user_count} USDT***', parse_mode='MARKDOWN')




@dp.message_handler(regexp='^0x[a-fA-F0-9]{64}$', content_types=['photo'])
async def handle_transaction_eth(message: Message):
    global succes_or_invalid, user_count
    print(user_count)
    user_id = message.from_user.id
    succes_or_invalid = InlineKeyboardMarkup(inline_keyboard=[(
        InlineKeyboardButton(text='✅Успешно', callback_data=f'success:{user_id}'),
        InlineKeyboardButton(text='❌Не успешно', callback_data=f'invalid:{user_id}')
    )])
    pay_k = succes_or_invalid
    await message.forward(chat_id=GROUP_CHAT_ID)
    await message.answer('✅Отлично! <b>Ваша заявка будет одобрена от 15 минут до 24 часов</b>\n\n'
                         '<b>Если</b> будут вопросы обращайтесь в поддержку: @pump_supporting_bot', parse_mode='html')
    await bot.send_message(GROUP_CHAT_ID, f'ETH {user_count} USDT', reply_markup=pay_k)


@dp.message_handler(regexp='[a-fA-F0-9]{64}$', content_types=['photo'])
async def handle_transaction_tron(message: Message):
    global succes_or_invalid, user_count
    print(user_count)
    user_id = message.from_user.id
    succes_or_invalid = InlineKeyboardMarkup(inline_keyboard=[(
        InlineKeyboardButton(text='✅Успешно', callback_data=f'success:{user_id}'),
        InlineKeyboardButton(text='❌Не успешно', callback_data=f'invalid:{user_id}')
    )])
    pay_k = succes_or_invalid
    await message.forward(chat_id=GROUP_CHAT_ID)
    await message.answer('✅Отлично! <b>Ваша заявка будет одобрена от 15 минут до 24 часов</b>\n\n'
                         '<b>Если</b> будут вопросы обращайтесь в поддержку: @pump_supporting_bot', parse_mode='html')
    await bot.send_message(GROUP_CHAT_ID, f'TRX {user_count} USDT', reply_markup=pay_k)


@dp.message_handler(regexp='[a-fA-F0-9]{66}$', content_types=['photo'])
async def handle_transaction_ton(message: Message):
    global succes_or_invalid, user_count
    print(user_count)
    user_id = message.from_user.id
    succes_or_invalid = InlineKeyboardMarkup(inline_keyboard=[(
        InlineKeyboardButton(text='✅Успешно', callback_data=f'success:{user_id}'),
        InlineKeyboardButton(text='❌Не успешно', callback_data=f'invalid:{user_id}')
    )])
    pay_k = succes_or_invalid
    await message.forward(chat_id=GROUP_CHAT_ID)
    await message.answer('✅Отлично! <b>Ваша заявка будет одобрена от 15 минут до 24 часов</b>\n\n'
                         '<b>Если</b> будут вопросы обращайтесь в поддержку: @pump_supporting_bot', parse_mode='html')
    await bot.send_message(GROUP_CHAT_ID, f'TON {user_count}', reply_markup=pay_k)






@dp.callback_query_handler(lambda query: True)
async def handle_callback(callback_query: CallbackQuery):
    global WALLET, NETWORK, sum
    try:
        action, user_id = callback_query.data.split(':')
        user_id = int(user_id)
        if action == 'success':
            db.set_user_wallet_make(user_id, sum)
            await bot.send_message(user_id, f'✅ Пополнение на кошелек прошло успешно!\n'
                                            f'💵 Кошелек: <b>{db.get_user_wallet(user_id)}₽</b>', parse_mode='html')

        if callback_query.data == 'invalid':
            await bot.answer_callback_query(callback_query.id)
            await bot.send_message(user_id,
                                   '❌Похоже что-то пошло не так: <b>возникла проблема с обработкой данных</b>\n'
                                   '<b>Если</b> вы уверены, что все данные верны обратитесь в поддержку: @pump_supporting_bot',
                                   parse_mode='html')
    except Exception as e:
        pass
    data = callback_query.data
    regions = [i for i in free_hosts]
    other_regions = [i for i in other_hosts]
    all_regions = regions + other_regions
    print(get_ms())
    print(regions)


    if data == 'connect_to_vpn':
        server_keyboard = InlineKeyboardMarkup(row_width=3)
        if db.get_sub_status(callback_query.from_user.id):
            for i in all_regions:
                button = InlineKeyboardButton(text=i, callback_data=i)
                server_keyboard.add(button)
            await callback_query.message.answer(
                f'{callback_query.from_user.first_name}, выбери сервер для подключения:', reply_markup=server_keyboard)
        else:
            for i in regions:
                button = InlineKeyboardButton(text=i, callback_data=i)
                server_keyboard.add(button)
            await callback_query.message.answer(
                f'{callback_query.from_user.first_name}, выбери сервер для подключения:', reply_markup=server_keyboard)



    if data in all_regions:
        if db.get_sub_status(callback_query.from_user.id):
            try:
                enable_message = await callback_query.message.answer(f'🤖 <b>Подключаюсь к серверу {data}...</b>',
                                                                     parse_mode='html')
                await asyncio.sleep(3)
                await enable_message.delete()
                run_request()
                enable_vpn(free_hosts[data]['ip'], free_hosts[data]['port'])
                run_request()
                await callback_query.message.answer(
                    f'🤖 VPN подключен успешно. Теперь ты можешь пользоваться {data}!\n\n'
                    f'🌎 Скорость сервера: <b>{get_ms()}ms</b>\n'
                    f'📶 Необходимо переподключиться через: <b>5 часов</b>', parse_mode='html')
            except Exception as e:
                await callback_query.message.answer(
                    '❌ <b>Ошибка в подключении!</b> Выберите другой сервер или переподключитесь позже', parse_mode='html')
        else:
            if data in regions:
                try:
                    enable_message = await callback_query.message.answer(f'🤖 <b>Подключаюсь к серверу {data}...</b>',
                                                                         parse_mode='html')
                    await asyncio.sleep(3)
                    await enable_message.delete()
                    run_request()
                    enable_vpn(free_hosts[data]['ip'], free_hosts[data]['port'])
                    run_request()
                    await callback_query.message.answer(
                        f'🤖 VPN подключен успешно. Теперь ты можешь пользоваться {data}!\n\n'
                        f'🌎 Скорость сервера: <b>{get_ms()}ms</b>\n'
                        f'📶 Необходимо переподключиться через: <b>5 часов</b>', parse_mode='html')
                except Exception as e:
                    await callback_query.message.answer('❌ Ошибка в подключении! Выберите другой сервер или переподключитесь позже', parse_mode='html')
            else:
                await callback_query.message.answer(
                    f'🚨 Доступ закончился! {callback_query.from_user.first_name}, нам нужно это исправить!\n\n'
                    f'🌎 <b>Пользуйся всеми серверами и без переподключения при оплате доступа!</b>\n\n', parse_mode='html')




    if data == 'view_profile':
        user_sub = time_sub_day(db.get_time_sub(callback_query.from_user.id))
        if user_sub == False:
            user_sub = '❌ <b>Отсутствует</b>'
        await callback_query.message.answer(f'👤 Профиль: {db.get_nickname(callback_query.from_user.id)}\n'
                                            f'├\n'
                                            f'├ 🔋 Подписка: <b>{user_sub}</b>\n'
                                            f'├ 📋 Ваши рефералы: <b>{db.get_count_refers(callback_query.from_user.id)}</b>\n'
                                            f'└ 💵 Кошелек: <b>{db.get_user_wallet(callback_query.from_user.id)}₽</b>', parse_mode='html', reply_markup=profile_keyboard)

    """Чтобы появился доступ к другим серверам нужно поплнить кошелек через кнопку ***ОПЛАТИТЬ ДОСТУП*** тогда кошелек пополнится"""

    if data == 'referal_system':
        await callback_query.message.answer(
            f'🤖 <b>За каждого приглашенного человека в бота вы получите 10₽ на кошелек!</b>\n\n🚀 Ваша реферальная ссылка: https://t.me/{BOT_NICKNAME}?start={callback_query.from_user.id}\n\n',
            parse_mode='html')




    if data == 'pay_the_bot':
        await callback_query.message.answer(f'🤖 Наш тариф:\n1 месяц = 500₽\n6 месяцев = 2500₽\n1 год = 5500₽\n\n<b>❗ Чтобы пополнить доступ нужно пополнить кошелек. Вы можете вводить промокоды от разработчика.</b>\n\n💵 Кошелек: <b>{db.get_user_wallet(callback_query.from_user.id)}₽</b>\n\nВыберите тариф:', reply_markup=payment_keyboard, parse_mode='html')

    if data == 'month':
            if float(db.get_user_wallet(callback_query.from_user.id)) >= 500:
                db.set_user_wallet_take(callback_query.from_user.id, 500)
                if db.get_sub_status(callback_query.from_user.id):
                    time_sub = int(time.time() + days_to_seconds(30)) - int(time.time())
                    db.set_time_sub(callback_query.from_user.id, time_sub)
                    await bot.send_message(callback_query.from_user.id, '✅ Вы успешно преобрели <b>доступ на 1 месяц</b>', parse_mode='html')
                else:
                    time_sub = int(time.time() + days_to_seconds(30))
                    db.set_time_sub(callback_query.from_user.id, time_sub)
                    await bot.send_message(callback_query.from_user.id, '✅ Вы успешно преобрели <b>доступ на 1 месяц</b>', parse_mode='html')
            else:
                await callback_query.message.answer(f'❌ Недостаточно средств на кошельке!', parse_mode='html', reply_markup=pay_the_loot_keyboard)

    if data == 'halfyear':
            if float(db.get_user_wallet(callback_query.from_user.id)) >= 2500:
                db.set_user_wallet_take(callback_query.from_user.id, 2500)
                if db.get_sub_status(callback_query.from_user.id):
                    time_sub = int(time.time() + days_to_seconds(180)) - int(time.time())
                    db.set_time_sub(callback_query.from_user.id, time_sub)
                    await bot.send_message(callback_query.from_user.id, '✅ Вы успешно преобрели <b>доступ на 6 месяцев</b>', parse_mode='html')
                else:
                    time_sub = int(time.time() + days_to_seconds(180))
                    db.set_time_sub(callback_query.from_user.id, time_sub)
                    await bot.send_message(callback_query.from_user.id, '✅ Вы успешно преобрели <b>доступ на 6 месяцев</b>', parse_mode='html')
            else:
                await callback_query.message.answer(f'❌ Недостаточно средств на кошельке!', parse_mode='html', reply_markup=pay_the_loot_keyboard)

    if data == 'year':
            if float(db.get_user_wallet(callback_query.from_user.id)) >= 5500:
                db.set_user_wallet_take(callback_query.from_user.id, 5500)
                if db.get_sub_status(callback_query.from_user.id):
                    time_sub = int(time.time() + days_to_seconds(365)) - int(time.time())
                    db.set_time_sub(callback_query.from_user.id, time_sub)
                    await bot.send_message(callback_query.from_user.id, '✅ Вы успешно преобрели <b>доступ на 1 год</b>', parse_mode='html')
                else:
                    time_sub = int(time.time() + days_to_seconds(365))
                    db.set_time_sub(callback_query.from_user.id, time_sub)
                    await bot.send_message(callback_query.from_user.id, '✅ Вы успешно преобрели <b>доступ на 1 год</b>', parse_mode='html')
            else:
                await callback_query.message.answer(f'❌ Недостаточно средств на кошельке!', parse_mode='html', reply_markup=pay_the_loot_keyboard)

    if data == 'bye_loot':
        await callback_query.message.answer('🤖 <b>Выбери сеть для оплаты USDT:</b>', parse_mode='html', reply_markup=network1)



    if data == 'TON':
        NETWORK = 'TON'
        WALLET = 'UQCZWX_JeVoi9ajcpXKAp1F8soOH2YIv6HitZeGUE16gGVfk'
        await callback_query.message.answer(
           '🤖 <b>Введите сумму на которую вы хотите пополнить на кошелек (в рублях):</b>', parse_mode='html')

    if data == 'TRC':
        NETWORK = 'TRC'
        WALLET = 'TWBv2DH5cpHP8UgRj9wdCcr2rWkJTgGJoo'
        await callback_query.message.answer(
            '🤖 <b>Введите сумму на которую вы хотите пополнить на кошелек (в рублях):</b>', parse_mode='html')

    if data == 'ERC':
        NETWORK = 'ERC'
        WALLET = '0x4B908f33111e968970bD4c5b1f6CE4014ad4F92E'
        await callback_query.message.answer(
            '🤖 <b>Введите сумму на которую вы хотите пополнить на кошелек (в рублях):</b>', parse_mode='html')




# Connecting to VPN (SOCKS5)
def enable_vpn(proxy_host, proxy_port):
    os.environ['HTTP_PROXY'] = f'socks5h://{proxy_host}:{proxy_port}'
    os.environ['HTTPS_PROXY'] = f'socks5h://{proxy_host}:{proxy_port}'

    threading.Timer(300 * 60, disable_vpn).start()

def disable_vpn():
    os.environ.pop('HTTP_PROXY', None)
    os.environ.pop('HTTPS_PROXY', None)

def run_request():
    response = requests.get("https://httpbin.org/ip", timeout=10)
    print(response.json())

def get_ms():
    ping = os.popen('ping www.google.com -n 1')
    result = ping.readlines()
    msLine = result[-1].strip()
    msLine2 = msLine.split(' = ')[-1]
    return str(msLine2)[0:3]


# run_request()
# enable_vpn(proxy_host, proxy_port)
# run_request()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)