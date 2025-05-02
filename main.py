from keyboards import main_keyboard, payment_keyboard1, profile_keyboard, payment_keyboard, pay_the_loot_keyboard, network1, success_or_invalid, back_command_keyboard
from aiogram.types import Message, CallbackQuery
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command, StateFilter
from aiogram import Bot
import re
import asyncio
from aiogram.types import FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton, ContentType
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import StatesGroup, State
import time
import json
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder


import asyncio
import requests
import os
import subprocess
from db import Database
import threading
import time
import datetime


bot = Bot('YOUR BOT TOKEN')
dp = Dispatcher(storage=MemoryStorage())
proxy_host = 'TEST PROXY HOST'
proxy_port = 'TEST PROXY PORT'
db = Database('database.db')

BOT_NICKNAME = 'YOUR BOT NICKNAME'
cost = ''
WALLET = 'YOUR CRYPTO WALLET'
NETWORK = ''
user_count = ''
GROUP_CHAT_ID = -1002192140565
sum = ''



class Renting(StatesGroup):
    rent_time = State()
    send_photo = State()



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

# РАСЧЕТ ПОДПИСКИ
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




# ПОДСЧЕТ РУБЛЕЙ В ДОЛЛАРЫ и наоборот
def calculate_sum_from_rubs_to_dollars(num):
    return round(num / 85.00, 2)


def calculate_sum_from_dollars_to_rubs(num):
    return round(num * 85.00, 2)



# ДЛЯ ВРЕМЕННОГО ФОТО
async def download_photo(file_id: str, path: str):
    file = await bot.get_file(file_id)
    await bot.download_file(file.file_path, path)




@dp.message(Command('start'))
async def start(message: Message):
    db.create_tables()
    black_photo_path = 'fotos/black.jpg'
    success_photo_path = 'fotos/success.jpg'
    error_photo_path = 'fotos/error.jpg'
    message_photo_path = 'fotos/message.jpg'

    await message.answer_photo(photo=FSInputFile(black_photo_path), caption=f"🤖 Привет, {message.from_user.first_name}! Я Pump VPN - помогу тебе обойти блокировку различных источников, которые недоступны в РФ и не только.", reply_markup=main_keyboard())
    # Проверка подписки на старте и выдача пробного доступа

    if (not db.user_exists(message.from_user.id)):
        db.add_user(message.from_user.id)
        db.set_nickname(message.from_user.id, message.from_user.username)
        db.set_signup(message.from_user.id, 'done')
        user_id = message.from_user.id

        if db.get_sub_status(user_id):
            time_sub = int(time.time() + days_to_seconds(1)) - int(time.time())
            db.set_time_sub(user_id, time_sub)
            await message.answer_photo(photo=FSInputFile(success_photo_path), caption=f'✅ <b>Вам был выдан пробный переод на 1 день</b>', parse_mode='html', reply_markup=back_command_keyboard())

        else:

            time_sub = int(time.time() + days_to_seconds(1))
            db.set_time_sub(user_id, time_sub)
            await message.answer_photo(photo=FSInputFile(success_photo_path), caption=f'✅ <b>Вам был выдан пробный период на 1 день</b>', parse_mode='html', reply_markup=back_command_keyboard())

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
                    await message.answer_photo(photo=FSInputFile(success_photo_path), caption=f'✅ <b>Вам был выдан пробный период на 1 день</b>', parse_mode='html', reply_markup=back_command_keyboard())

                else:
                    time_sub = int(time.time() + days_to_seconds(1))
                    db.set_time_sub(user_id, time_sub)
                    await message.answer_photo(photo=FSInputFile(success_photo_path), caption=f'✅ <b>Вам был выдан пробный период на 1 день</b>', parse_mode='html', reply_markup=back_command_keyboard())

                try:
                    await bot.send_photo(referrer_id, photo=FSInputFile(message_photo_path),
                                           caption="✅ <b>По вашей ссылке зарегистрировался новый пользователь.</b>\n\n <i>Кошелек пополнен на 10₽</i>\n\n", parse_mode='html', reply_markup=back_command_keyboard())
                    db.set_user_wallet_make(referrer_id, 10)
                    db.set_count_refers(referrer_id)
                    """
                    Можно добавить бонус на 10 дней доступа 
                    """
                except:
                    pass
            else:
                pass
        else:
            pass
    else:
        if db.get_sub_status(message.from_user.id):
            await message.answer_photo(photo=FSInputFile(success_photo_path), caption='✅ ***Есть доступ к боту***', parse_mode='MARKDOWN', reply_markup=back_command_keyboard())

        else:
            await message.answer_photo(photo=FSInputFile(error_photo_path), caption=
                f'🚨 Доступ закончился! {message.from_user.first_name}, нам нужно это исправить!\n\n'
                f'🌎 <b>Пользуйся всеми серверами и без переподключения при оплате доступа!</b>',
                reply_markup=payment_keyboard1(), parse_mode='html')




# # ЗАПРОС НА СУММУ ПОПОЛНЕНИЯ КОШЕЛЬКА
# @dp.message(content_types=['text'])
# async def loot_for_wallet(message: Message):
#     global cost, user_count, sum
#     if message.text.isdigit():
#         sum = int(message.text)
#         user_count = calculate_sum_from_rubs_to_dollars(sum)
#         await message.answer(f'🤖 ***Переведите сумму ниже на адрес кошелька:***\n\n'
#                              f'`{WALLET}`\n\n'
#                              f'❗ ***Потом пришлите пришлите скриншот оплаты. В описании под скриншотом нужно вставить хэш транзакции, иначе бот не засчитает оплату. (сеть {NETWORK})***\n\n'
#                              f'💵 К оплате: ***{user_count} USDT***', parse_mode='MARKDOWN')



# @dp.message(regexp='^0x[a-fA-F0-9]{64}$', content_types=['photo'])
# async def handle_transaction_eth(message: Message):
#     global succes_or_invalid, user_count
#     print(user_count)
#     user_id = message.from_user.id
#     succes_or_invalid = InlineKeyboardMarkup(inline_keyboard=[(
#         InlineKeyboardButton(text='✅Успешно', callback_data=f'success:{user_id}'),
#         InlineKeyboardButton(text='❌Не успешно', callback_data=f'invalid:{user_id}')
#     )])
#     pay_k = succes_or_invalid
#     await message.forward(chat_id=GROUP_CHAT_ID)
#     await message.answer('✅Отлично! <b>Ваша заявка будет одобрена от 15 минут до 24 часов</b>\n\n'
#                          '<b>Если</b> будут вопросы обращайтесь в поддержку: @pump_supporting_bot', parse_mode='html')
#     await bot.send_message(GROUP_CHAT_ID, f'ETH {user_count} USDT', reply_markup=pay_k)
#
#
# @dp.message_handler(regexp='[a-fA-F0-9]{64}$', content_types=['photo'])
# async def handle_transaction_tron(message: Message):
#     global succes_or_invalid, user_count
#     print(user_count)
#     user_id = message.from_user.id
#     succes_or_invalid = InlineKeyboardMarkup(inline_keyboard=[(
#         InlineKeyboardButton(text='✅Успешно', callback_data=f'success:{user_id}'),
#         InlineKeyboardButton(text='❌Не успешно', callback_data=f'invalid:{user_id}')
#     )])
#     pay_k = succes_or_invalid
#     await message.forward(chat_id=GROUP_CHAT_ID)
#     await message.answer('✅Отлично! <b>Ваша заявка будет одобрена от 15 минут до 24 часов</b>\n\n'
#                          '<b>Если</b> будут вопросы обращайтесь в поддержку: @pump_supporting_bot', parse_mode='html')
#     await bot.send_message(GROUP_CHAT_ID, f'TRX {user_count} USDT', reply_markup=pay_k)
#
#
# @dp.message_handler(regexp='[a-fA-F0-9]{66}$', content_types=['photo'])
# async def handle_transaction_ton(message: Message):
#     global succes_or_invalid, user_count
#     print(user_count)
#     user_id = message.from_user.id
#     succes_or_invalid = InlineKeyboardMarkup(inline_keyboard=[(
#         InlineKeyboardButton(text='✅Успешно', callback_data=f'success:{user_id}'),
#         InlineKeyboardButton(text='❌Не успешно', callback_data=f'invalid:{user_id}')
#     )])
#     pay_k = succes_or_invalid
#     await message.forward(chat_id=GROUP_CHAT_ID)
#     await message.answer('✅Отлично! <b>Ваша заявка будет одобрена от 15 минут до 24 часов</b>\n\n'
#                          '<b>Если</b> будут вопросы обращайтесь в поддержку: @pump_supporting_bot', parse_mode='html')
#     await bot.send_message(GROUP_CHAT_ID, f'TON {user_count}', reply_markup=pay_k)






@dp.callback_query(lambda F: True)
async def handle_callback(callback_query: CallbackQuery, state: FSMContext):
    global WALLET, NETWORK, sum
    message_photo_path = 'fotos/message.jpg'
    error_photo_path = 'fotos/error.jpg'
    lighting_photo_path = 'fotos/lightning.jpg'
    success_photo_path = 'fotos/success.jpg'
    black_photo_path = 'fotos/black.jpg'
    profile_photo_path = 'fotos/profile.jpg'
    referal_photo_path = 'fotos/invite.jpg'
    bank_photo_path = 'fotos/bank.jpg'
    card_photo_path = 'fotos/bank_cards.jpg'


    # ПРОВЕРКА ОПЛАТЫ
    try:
        action, user_id = callback_query.data.split(':')
        user_id = int(user_id)
        rent = float(db.get_rent(user_id))
        print(rent)
        if action == 'success':
            new_rent = calculate_sum_from_dollars_to_rubs(rent)
            print(new_rent)
            db.set_user_wallet_make(user_id, new_rent)
            await bot.send_photo(photo=FSInputFile(message_photo_path), chat_id=user_id,
                                     caption=f'✅ <b>Пополнение на кошелек прошло успешно!</b>\n\n'
                                             f'💵 Кошелек: <b>{db.get_user_wallet(user_id)}₽</b>', parse_mode='html',
                                     reply_markup=back_command_keyboard())

        if action == 'invalid':
            await bot.answer_callback_query(callback_query.id)
            await bot.send_photo(photo=FSInputFile(error_photo_path), chat_id=user_id,
                                    caption='❌ <b>Похоже что-то пошло не так. Возможно возникла проблема с обработкой данных.</b>\n\n'
                                             '<i>Если вы уверены, что все данные верны обратитесь в поддержку: @pump_supporting_bot</i>',
                                    parse_mode='html', reply_markup=back_command_keyboard())
    except Exception as e:
        pass


    data = callback_query.data
    regions = [i for i in free_hosts]
    other_regions = [i for i in other_hosts]
    all_regions = regions + other_regions

    # ВЫБОР СЕРВЕРА
    if data == 'connect_to_vpn':
        server_keyboard = InlineKeyboardBuilder()
        if db.get_sub_status(callback_query.from_user.id):

            for i in all_regions:
                button = InlineKeyboardButton(text=i, callback_data=i)
                server_keyboard.add(button)

            await callback_query.message.answer_photo(
                photo=FSInputFile(lighting_photo_path), caption=f'{callback_query.from_user.first_name}, ***выбери сервер для подключения:***', reply_markup=server_keyboard.as_markup(), parse_mode='MARKDOWN')

        else:

            for i in regions:
                button = InlineKeyboardButton(text=i, callback_data=i)
                server_keyboard.add(button)

            await callback_query.message.answer_photo(
                photo=FSInputFile(lighting_photo_path),
                caption=f'{callback_query.from_user.first_name}, ***выбери сервер для подключения:***',
                reply_markup=server_keyboard.as_markup(), parse_mode='MARKDOWN')




    # ПРОВЕРКА ПОДКЛЮЧЕНИЯ
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

                await callback_query.message.answer_photo(photo=FSInputFile(success_photo_path), caption=
                    f'🤖 VPN подключен успешно. Теперь ты можешь пользоваться {data}!\n\n'
                    f'🌎 Скорость сервера: <b>{get_ms()}ms</b>\n'
                    f'📶 Необходимо переподключиться через: <b>5 часов</b>', parse_mode='html', reply_markup=back_command_keyboard())

            except Exception as e:
                await callback_query.message.answer_photo(photo=FSInputFile(error_photo_path), caption=
                    '❌ <b>Ошибка в подключении!</b> Выберите другой сервер или переподключитесь позже.', parse_mode='html', reply_markup=back_command_keyboard())

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

                    await callback_query.message.answer_photo(photo=FSInputFile(success_photo_path), caption=
                    f'🤖 VPN подключен успешно. Теперь ты можешь пользоваться {data}!\n\n'
                    f'🌎 Скорость сервера: <b>{get_ms()}ms</b>\n'
                    f'📶 Необходимо переподключиться через: <b>5 часов</b>', parse_mode='html',
                                                              reply_markup=back_command_keyboard())

                except Exception as e:
                    await callback_query.message.answer_photo(photo=FSInputFile(error_photo_path), caption=
                    '❌ <b>Ошибка в подключении!</b> Выберите другой сервер или переподключитесь позже.',
                                                              parse_mode='html', reply_markup=back_command_keyboard())

            else:
                await callback_query.message.answer(
                    f'🚨 Доступ закончился! {callback_query.from_user.first_name}, нам нужно это исправить!\n\n'
                    f'🌎 <b>Пользуйся всеми серверами и без переподключения при оплате доступа!</b>\n\n', parse_mode='html')


    # BACK COMMAND
    if data == 'back_to_menu':
        await callback_query.message.delete()
        await callback_query.message.answer_photo(photo=FSInputFile(black_photo_path), caption=f"🤖 Привет, {callback_query.message.from_user.first_name}! Я Pump VPN - помогу тебе обойти блокировку различных источников, которые недоступны в РФ и не только.", reply_markup=main_keyboard())



    # ПРОФИЛЬ ПОЛЬЗОВАТЕЛЯ
    if data == 'view_profile':
        user_sub = time_sub_day(db.get_time_sub(callback_query.from_user.id))
        if user_sub == False:
            user_sub = '❌ <b>Отсутствует</b>'
        await callback_query.message.answer_photo(photo=FSInputFile(profile_photo_path),
                                                  caption=f'👨‍💻 ***Ваш кабинет:***\n'
                                                          f'• Ваш никнейм: {callback_query.from_user.first_name}\n'
                                                          f'• Ваш ID: {callback_query.message.from_user.id}\n\n'
                                                          f'📊 ***Статистика:***\n'
                                                          f'↳ 👤 Рефералов: ***{db.get_count_refers(callback_query.from_user.id)}***\n'
                                                          f'↳ 🔋 Подписка: ***{user_sub}***\n\n'
                                                          f'💳 ***Баланс:***\n'
                                                          f'↳ 💰 Кошелек: ***{db.get_user_wallet(callback_query.from_user.id)}₽***\n\n'
                                                          f'👤 ***Реферальная ссылка:***\n'
                                                          f' ↳ ___За каждого приглашенного человека в бота вы получите 10 Дней Доступа!___\n\n'
                                                          f'🚀 Ваша реферальная ссылка: [Ссылка](https://t.me/{BOT_NICKNAME}?start={callback_query.from_user.id})',
                                                  parse_mode='MARKDOWN', reply_markup=payment_keyboard1())


    """Чтобы появился доступ к другим серверам нужно поплнить кошелек через кнопку ***ПОПОЛНИТЬ КОШЕЛЕК*** тогда кошелек пополнится,
    затем пополнить доступ по кнопке ***ПОПОЛНИТЬ ДОСТУП***. Теперь можно пользоваться серверами."""


    if data == 'referal_system':
        await callback_query.message.answer_photo(photo=FSInputFile(referal_photo_path),
                                                  caption=f'🧑‍🧑‍🧒 <b>Партнёры</b> — это люди, которые перешли по вашей ссылке и начали пользоваться данным ботом.\n\n'
                                                          f'🤖 <b>За каждого приглашенного человека в бота вы получите 10 Дней доступа!</b>\n\n🚀 <b>Ваша реферальная ссылка:</b> https://t.me/{BOT_NICKNAME}?start={callback_query.from_user.id}\n\n'
                                                          f'👥 <b>Вы пригласили партнеров:</b> {db.get_count_refers(callback_query.from_user.id)}\n\n'
                                                          f'<i>Приводи друзей - зарабатывайте вместе!</i>',
                                                  parse_mode='html', reply_markup=back_command_keyboard())



    # ПОПОЛНЕНИЕ КОШЕЛЬКА И ДОСТУПА
    if data == 'pay_the_bot':
        await callback_query.message.answer_photo(photo=FSInputFile(bank_photo_path),
                                                              caption=f'🤖 Наш тариф:\n1 месяц = 500 ₽\n6 месяцев = 2500 ₽\n1 год = 5500 ₽\n\n<b>❗ Чтобы пополнить доступ нужно пополнить кошелек. Вы можете вводить промокоды от разработчика.</b>\n\n💵 Кошелек: <b>{db.get_user_wallet(callback_query.from_user.id)} USDT</b>\n\n<i>Выберите тариф:</i>',
                                                              reply_markup=payment_keyboard(), parse_mode='html')

    if data == 'month':
        if float(db.get_user_wallet(callback_query.from_user.id)) >= 500:
            db.set_user_wallet_take(callback_query.from_user.id, 500)
            if db.get_sub_status(callback_query.from_user.id):
                time_sub = int(time.time() + days_to_seconds(30)) - int(time.time())
                db.set_time_sub(callback_query.from_user.id, time_sub)
                await bot.send_photo(photo=FSInputFile(success_photo_path), chat_id=callback_query.from_user.id,
                                                         caption='✅ <b>Вы успешно преобрели доступ на 1 месяц</b>\n\n'
                                                                 '<i>🎉 Поздравляем!</i>', parse_mode='html', reply_markup=back_command_keyboard())
            else:
                time_sub = int(time.time() + days_to_seconds(30))
                db.set_time_sub(callback_query.from_user.id, time_sub)
                await bot.send_photo(photo=FSInputFile(success_photo_path), chat_id=callback_query.from_user.id,
                                     caption='✅ <b>Вы успешно преобрели доступ на 1 месяц</b>\n\n'
                                             '<i>🎉 Поздравляем!</i>', parse_mode='html',
                                     reply_markup=back_command_keyboard())
        else:
            await callback_query.message.answer_photo(photo=FSInputFile(success_photo_path),
                                                                      caption=f'❌ <b>Недостаточно средств на кошельке!</b>\n\n'
                                                                              f'<i>👇 Пополните кошелек по кнопке ниже чтобы оплатить доступ!</i>',
                                                                      parse_mode='html',
                                                                      reply_markup=payment_keyboard1())


    if data == 'halfyear':
        if float(db.get_user_wallet(callback_query.from_user.id)) >= 2500:
            db.set_user_wallet_take(callback_query.from_user.id, 2500)
            if db.get_sub_status(callback_query.from_user.id):
                time_sub = int(time.time() + days_to_seconds(180)) - int(time.time())
                db.set_time_sub(callback_query.from_user.id, time_sub)
                await bot.send_photo(photo=FSInputFile(success_photo_path), chat_id=callback_query.from_user.id,
                                     caption='✅ <b>Вы успешно преобрели доступ на 6 месяцев</b>\n\n'
                                             '<i>🎉 Поздравляем!</i>', parse_mode='html',
                                     reply_markup=back_command_keyboard())
            else:
                time_sub = int(time.time() + days_to_seconds(180))
                db.set_time_sub(callback_query.from_user.id, time_sub)
                await bot.send_photo(photo=FSInputFile(success_photo_path), chat_id=callback_query.from_user.id,
                                     caption='✅ <b>Вы успешно преобрели доступ на 6 месяцев</b>\n\n'
                                             '<i>🎉 Поздравляем!</i>', parse_mode='html',
                                     reply_markup=back_command_keyboard())
        else:
            await callback_query.message.answer_photo(photo=FSInputFile(success_photo_path),
                                                      caption=f'❌ <b>Недостаточно средств на кошельке!</b>\n\n'
                                                              f'<i>👇 Пополните кошелек по кнопке ниже чтобы оплатить доступ!</i>',
                                                      parse_mode='html',
                                                      reply_markup=payment_keyboard1())



    if data == 'year':
        if float(db.get_user_wallet(callback_query.from_user.id)) >= 5500:
            db.set_user_wallet_take(callback_query.from_user.id, 5500)
            if db.get_sub_status(callback_query.from_user.id):
                time_sub = int(time.time() + days_to_seconds(365)) - int(time.time())
                db.set_time_sub(callback_query.from_user.id, time_sub)
                await bot.send_photo(photo=FSInputFile(success_photo_path), chat_id=callback_query.from_user.id,
                                     caption='✅ <b>Вы успешно преобрели доступ на 1 год</b>\n\n'
                                             '<i>🎉 Поздравляем!</i>', parse_mode='html',
                                     reply_markup=back_command_keyboard())
            else:
                time_sub = int(time.time() + days_to_seconds(365))
                db.set_time_sub(callback_query.from_user.id, time_sub)
                await bot.send_photo(photo=FSInputFile(success_photo_path), chat_id=callback_query.from_user.id,
                                     caption='✅ <b>Вы успешно преобрели доступ на 1 год</b>\n\n'
                                             '<i>🎉 Поздравляем!</i>', parse_mode='html',
                                     reply_markup=back_command_keyboard())
        else:
            await callback_query.message.answer_photo(photo=FSInputFile(success_photo_path),
                                                      caption=f'❌ <b>Недостаточно средств на кошельке!</b>\n\n'
                                                              f'<i>👇 Пополните кошелек по кнопке ниже чтобы оплатить доступ!</i>',
                                                      parse_mode='html',
                                                      reply_markup=payment_keyboard1())



    if data == 'bye_loot':
        await callback_query.message.answer_photo(photo=FSInputFile(card_photo_path),
                                                              caption='🤖 <b>Выбери сеть для оплаты USDT:</b>',
                                                              parse_mode='html',
                                                              reply_markup=network1())



    # if data == 'TON':
    #     NETWORK = 'TON'
    #     WALLET = 'UQCZWX_JeVoi9ajcpXKAp1F8soOH2YIv6HitZeGUE16gGVfk'
    #     await callback_query.message.answer(
    #        '🤖 <b>Введите сумму на которую вы хотите пополнить на кошелек (в рублях):</b>', parse_mode='html')
    #
    # if data == 'TRC':
    #     NETWORK = 'TRC'
    #     WALLET = 'TWBv2DH5cpHP8UgRj9wdCcr2rWkJTgGJoo'
    #     await callback_query.message.answer(
    #         '🤖 <b>Введите сумму на которую вы хотите пополнить на кошелек (в рублях):</b>', parse_mode='html')
    #
    # if data == 'ERC':
    #     NETWORK = 'ERC'
    #     WALLET = '0x4B908f33111e968970bD4c5b1f6CE4014ad4F92E'
    #     await callback_query.message.answer(
    #         '🤖 <b>Введите сумму на которую вы хотите пополнить на кошелек (в рублях):</b>', parse_mode='html')




    if data == 'TON':
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
        db.set_wallet(callback_query.from_user.id, 'UQCZWX_JeVoi9ajcpXKAp1F8soOH2YIv6HitZeGUE16gGVfk')
        db.set_network(callback_query.from_user.id, 'TON')
        await state.set_state(Renting.rent_time)
        await callback_query.message.answer_photo(photo=FSInputFile(card_photo_path),
                                                          caption='🤖 <b>Введите сумму которую вы хотите пополнить на кошелек (в рублях, без точек и запятых):</b>',
                                                          parse_mode='html', reply_markup=back_command_keyboard())

    if data == 'TRC':
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
        db.set_wallet(callback_query.from_user.id, 'TWBv2DH5cpHP8UgRj9wdCcr2rWkJTgGJoo')
        db.set_network(callback_query.from_user.id, 'TRC')
        await state.set_state(Renting.rent_time)
        await callback_query.message.answer_photo(photo=FSInputFile(card_photo_path),
                                                      caption='🤖 <b>Введите сумму которую вы хотите пополнить на кошелек (в рублях, без точек и запятых):</b>',
                                                      parse_mode='html', reply_markup=back_command_keyboard())

    if data == 'ERC':
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
        db.set_wallet(callback_query.from_user.id, '0x4B908f33111e968970bD4c5b1f6CE4014ad4F92E')
        db.set_network(callback_query.from_user.id, 'ERC')
        await state.set_state(Renting.rent_time)
        await callback_query.message.answer_photo(photo=FSInputFile(card_photo_path),
                                                          caption='🤖 <b>Введите сумму которую вы хотите пополнить на кошелек (в рублях, без точек и запятых):</b>',
                                                          parse_mode='html', reply_markup=back_command_keyboard())



# БЛОК ОПЛАТЫ
@dp.message(Renting.rent_time)
async def loot_for_wallet(message: types.Message, state: FSMContext):
    bank_photo_path = 'fotos/bank.jpg'
    if message.text.isdigit():
        await state.clear()
        await state.set_state(Renting.send_photo)
        user_count = calculate_sum_from_rubs_to_dollars(float(message.text))
        db.set_rent(message.from_user.id, user_count)
        await message.answer_photo(photo=FSInputFile(bank_photo_path), caption=f'🤖 ***Переведите сумму ниже на адрес кошелька:***\n\n'
                             f'`{db.get_wallet(message.from_user.id)}`\n\n'
                             f'❗ ***Потом пришлите пришлите скриншот оплаты. В описании под скриншотом нужно вставить хэш транзакции, иначе бот не засчитает оплату. (сеть {db.get_network(message.from_user.id)})***\n\n'
                             f'💵 К оплате: ***{db.get_rent(message.from_user.id)} USDT ≈ {float(message.text)}₽*** ', parse_mode='MARKDOWN', reply_markup=back_command_keyboard())




# PAYMENT_PART; TON; TRX; eth;
# ОБРАБАТЫВАЕМ ХЭШИ И ПЕРЕСЫЛАЕМ СООБЩЕНИЯ В НАШУ ГРУППУ
@dp.message(F.photo, Renting.send_photo)
async def transaction_handle(message: types.Message, state: FSMContext):
    error_photo_path = 'fotos/error.jpg'

    # ПРОВРКА ХЭША: ETH;
    try:
        user = message.from_user.username or message.from_user.full_name

        if message.caption is None:
            await message.answer_photo(photo=FSInputFile(error_photo_path),
                                       caption='❗ ***Пожалуйста, вставьте в описание под фото хеш транзакции.***',
                                       parse_mode='MARKDOWN', reply_markup=back_command_keyboard())
            return

        if re.match(r'^0x[a-fA-F0-9]{64}$', message.caption) or re.match(r'^[a-fA-F0-9]{64}$', message.caption) or re.match(r'^[a-fA-F0-9]{66}$', message.caption):
            await state.clear()

            success_photo_path = 'fotos/success.jpg'
            user_id = message.from_user.id
            def succes_or_invalid2():
                builder = InlineKeyboardBuilder()
                builder.add(
                    InlineKeyboardButton(text='✅ Успешно', callback_data=f'success:{user_id}'),
                    InlineKeyboardButton(text='❌ Не успешно', callback_data=f'invalid:{user_id}')
                )
                builder.adjust(2)
                return builder.as_markup()


            # Сохраняем в папку user_photos (временно)
            await download_photo(message.photo[-1].file_id, f"user_photos/{message.photo[-1].file_id}.jpg")


            pay_k = succes_or_invalid2()

            # ОТПРАВКА СООБЩЕНИЯ ПОЛЬЗОВАТЕЛЯ В ГРУППУ
            await message.answer_photo(photo=FSInputFile(success_photo_path), caption='✅ <b>Отлично! Ваша заявка будет одобрена от 15 минут до 24 часов</b>\n\n'
                                     '<i>Если будут вопросы обращайтесь в поддержку: @your_bot</i>', parse_mode='html', reply_markup=back_command_keyboard())

            # await bot.send_photo(photo=FSInputFile(f'user_photos/{message.photo[-1].file_id}.jpg'), chat_id=GROUP_CHAT_ID, caption=f'***🔔 Сообщение об оплате:***\n\n NETWORK: ***{db.get_network(message.from_user.id)}***\n PRICE: ***{db.get_rent(message.from_user.id)} USDT***\n FROM USER: {user}\n HASh: `{message.caption}`', reply_markup=pay_k, parse_mode='MARKDOWN')
            await bot.send_photo(photo=FSInputFile(f'user_photos/{message.photo[-1].file_id}.jpg'), chat_id=GROUP_CHAT_ID, caption=f'<b>🔔 Сообщение об оплате:</b>\n\n NETWORK: <b>{db.get_network(message.from_user.id)}</b>\n PRICE: <b>{db.get_rent(message.from_user.id)} USDT</b>\n FROM USER: @{user}\n HASh: <code>{message.caption}</code>', reply_markup=pay_k, parse_mode='html')


            # УДАЛЯЕМ ВРЕМЕННОЕ ФОТО
            os.remove(f'user_photos/{message.photo[-1].file_id}.jpg')
        else:
            await message.answer_photo(photo=FSInputFile(error_photo_path),
                                       caption='❗ ***Пожалуйста, вставьте в описание под фото хеш транзакции.***',
                                       parse_mode='MARKDOWN', reply_markup=back_command_keyboard())
            return

    except Exception as e:
        print(e)






# # VIEW PROFILE
#     if callback_query.data == 'my_acc':
#         user_sub = time_sub_day(db.get_time_sub(callback_query.from_user.id))
#         if user_sub == False:
#             user_sub = '❌ ***Отсутствует***'
#         user_sub = f'***{user_sub}***'
#
#         profile_photo_path = 'fotos/profile.jpg'
#         await callback_query.message.answer_photo(photo=FSInputFile(profile_photo_path), caption=f'👨‍💻 ***Ваш кабинет:***\n'
#                                                                                         f'• Ваш никнейм: {callback_query.from_user.first_name}\n'
#                                                                                         f'• Ваш ID: {callback_query.message.from_user.id}\n\n'
#                                                                                         f'📊 ***Статистика:***\n'
#                                                                                         f'↳ 👤 Рефералов: ***{db.get_count_refers(callback_query.from_user.id)}***\n'
#                                                                                         f'↳ 🔋 Подписка: ***{user_sub}***\n\n'
#                                                                                         f'💳 ***Баланс:***\n'
#                                                                                         f'↳ 💰 Кошелек: ***{db.get_user_wallet(callback_query.from_user.id)}***\n\n'
#                                                                                         f'👤 ***Реферальная ссылка:***\n'
#                                                                                         f' ↳ ___За каждого приглашенного человека в бота вы получите 10 Дней Доступа!___\n\n'
#                                                                                         f'🚀 Ваша реферальная ссылка: [Ссылка](https://t.me/{BOT_NICKNAME}?start={callback_query.from_user.id})', parse_mode='MARKDOWN', reply_markup=payment_keyboard1())
#
#
#     if callback_query.data == 'partners_refs':
#         refferal_photo_path = 'fotos/invite.jpg'
#         await callback_query.message.answer_photo(photo=FSInputFile(refferal_photo_path),
#                                                   caption=f'🧑‍🧑‍🧒 <b>Партнёры</b> — это люди, которые перешли по вашей ссылке и начали пользоваться данным ботом.\n\n'
#                                                           f'🤖 <b>За каждого приглашенного человека в бота вы получите 10 Дней доступа!</b>\n\n🚀 <b>Ваша реферальная ссылка:</b> https://t.me/{BOT_NICKNAME}?start={callback_query.from_user.id}\n\n'
#                                                           f'👥 <b>Вы пригласили партнеров:</b> {db.get_count_refers(callback_query.from_user.id)}\n\n'
#                                                           f'<i>Приводи друзей - зарабатывайте вместе!</i>',
#                                                   parse_mode='html', reply_markup=back_command_keyboard())
#
#
#     # REFERAL SISTEM
#     # ПОПОЛНЕНИЕ КОШЕЛЬКА
#     if callback_query.data == 'pay_the_call':
#         bank_photo_path = 'fotos/bank.jpg'
#         await callback_query.message.answer_photo(photo=FSInputFile(bank_photo_path),
#                                                       caption=f'🤖 Наш тариф:\n1 месяц = 1 USDT\n6 месяцев = 5 USDT\n1 год = 10 USDT\n\n<b>❗ Чтобы пополнить доступ нужно пополнить кошелек. Вы можете вводить промокоды от разработчика.</b>\n\n💵 Кошелек: <b>{db.get_user_wallet(callback_query.from_user.id)} USDT</b>\n\n<i>Выберите тариф:</i>',
#                                                       reply_markup=payment_keyboard(), parse_mode='html')
#
#     if callback_query.data == 'month':
#             success_photo_path = 'fotos/success.jpg'
#             fail_photo_path = 'fotos/error.jpg'
#             if float(db.get_user_wallet(callback_query.from_user.id)) >= 1:
#                 db.set_user_wallet_take(callback_query.from_user.id, 1)
#                 if db.get_sub_status(callback_query.from_user.id):
#                     time_sub = int(time.time() + days_to_seconds(30)) - int(time.time())
#                     db.set_time_sub(callback_query.from_user.id, time_sub)
#                     await bot.send_photo(photo=FSInputFile(success_photo_path), chat_id=callback_query.from_user.id,
#                                          caption='✅ <b>Вы успешно преобрели доступ на 1 месяц</b>\n\n'
#                                                  '<i>🎉 Поздравляем!</i>', parse_mode='html', reply_markup=back_command_keyboard())
#                 else:
#                     time_sub = int(time.time() + days_to_seconds(30))
#                     db.set_time_sub(callback_query.from_user.id, time_sub)
#                     await bot.send_photo(photo=FSInputFile(success_photo_path), chat_id=callback_query.from_user.id,
#                                          caption='✅ <b>Вы успешно преобрели доступ на 1 месяц</b>\n\n'
#                                                  '<i>🎉 Поздравляем!</i>', parse_mode='html', reply_markup=back_command_keyboard())
#             else:
#                 await callback_query.message.answer_photo(photo=FSInputFile(success_photo_path),
#                                                           caption=f'❌ <b>Недостаточно средств на кошельке!</b>\n\n'
#                                                                   f'<i>👇 Пополните кошелек по кнопке ниже чтобы оплатить доступ!</i>',
#                                                           parse_mode='html',
#                                                           reply_markup=payment_keyboard1())
#
#     if callback_query.data == 'halfyear':
#             success_photo_path = 'fotos/success.jpg'
#             fail_photo_path = 'fotos/error.jpg'
#             if float(db.get_user_wallet(callback_query.from_user.id)) >= 5:
#                 db.set_user_wallet_take(callback_query.from_user.id, 5)
#                 if db.get_sub_status(callback_query.from_user.id):
#                     time_sub = int(time.time() + days_to_seconds(180)) - int(time.time())
#                     db.set_time_sub(callback_query.from_user.id, time_sub)
#                     await bot.send_photo(photo=FSInputFile(success_photo_path), chat_id=callback_query.from_user.id,
#                                          caption='✅ <b>Вы успешно преобрели доступ на 6 месяцев</b>\n\n'
#                                                  '<i>🎉 Поздравляем!</i>', parse_mode='html', reply_markup=back_command_keyboard())
#                 else:
#                     time_sub = int(time.time() + days_to_seconds(180))
#                     db.set_time_sub(callback_query.from_user.id, time_sub)
#                     await bot.send_photo(photo=FSInputFile(success_photo_path), chat_id=callback_query.from_user.id,
#                                          caption='✅ <b>Вы успешно преобрели доступ на 6 месяцев</b>\n\n'
#                                                  '<i>🎉 Поздравляем!</i>', parse_mode='html', reply_markup=back_command_keyboard())
#             else:
#                 await callback_query.message.answer_photo(photo=FSInputFile(fail_photo_path),
#                                                           caption=f'❌ <b>Недостаточно средств на кошельке!</b>\n\n'
#                                                                   f'<i>👇 Пополните кошелек по кнопке ниже чтобы оплатить доступ!</i>',
#                                                           parse_mode='html', reply_markup=payment_keyboard1())
#
#     if callback_query.data == 'year':
#             success_photo_path = 'fotos/success.jpg'
#             fail_photo_path = 'fotos/error.jpg'
#             if float(db.get_user_wallet(callback_query.from_user.id)) >= 10:
#                 db.set_user_wallet_take(callback_query.from_user.id, 10)
#                 if db.get_sub_status(callback_query.from_user.id):
#                     time_sub = int(time.time() + days_to_seconds(365)) - int(time.time())
#                     db.set_time_sub(callback_query.from_user.id, time_sub)
#                     await bot.send_photo(photo=FSInputFile(success_photo_path), chat_id=callback_query.from_user.id,
#                                          caption='✅ <b>Вы успешно преобрели доступ на 1 год</b>\n\n'
#                                                  '<i>🎉 Поздравляем!</i>', parse_mode='html', reply_markup=back_command_keyboard())
#                 else:
#                     time_sub = int(time.time() + days_to_seconds(365))
#                     db.set_time_sub(callback_query.from_user.id, time_sub)
#                     await bot.send_photo(photo=FSInputFile(success_photo_path), chat_id=callback_query.from_user.id,
#                                          caption='✅ <b>Вы успешно преобрели доступ на 1 год</b>\n\n'
#                                                  '<i>🎉 Поздравляем!</i>', parse_mode='html', reply_markup=back_command_keyboard())
#             else:
#                 await callback_query.message.answer_photo(photo=FSInputFile(fail_photo_path),
#                                                           caption=f'❌ <b>Недостаточно средств на кошельке!</b>\n\n'
#                                                                   f'<i>👇 Пополните кошелек по кнопке ниже чтобы оплатить доступ!</i>',
#                                                           parse_mode='html', reply_markup=payment_keyboard1())
#
#     if callback_query.data == 'bye_loot':
#             card_photo_path = 'fotos/bank_cards.jpg'
#             await callback_query.message.answer_photo(photo=FSInputFile(card_photo_path),
#                                                       caption='🤖 <b>Выбери сеть для оплаты USDT:</b>',
#                                                       parse_mode='html',
#                                                       reply_markup=network_keyboard())
#
#     if callback_query.data == 'TON':
#             await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
#             card_photo_path = 'fotos/bank_cards.jpg'
#             db.set_wallet(callback_query.from_user.id, 'UQCZWX_JeVoi9ajcpXKAp1F8soOH2YIv6HitZeGUE16gGVfk')
#             db.set_network(callback_query.from_user.id, 'TON')
#             await state.set_state(Renting.rent_time)
#             await callback_query.message.answer_photo(photo=FSInputFile(card_photo_path),
#                                                       caption='🤖 <b>Введите сумму которую вы хотите пополнить на кошелек (в USDT, без точек и запятых):</b>',
#                                                       parse_mode='html', reply_markup=back_command_keyboard())
#
#     if callback_query.data == 'TRC':
#             await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
#             card_photo_path = 'fotos/bank_cards.jpg'
#             db.set_wallet(callback_query.from_user.id, 'TWBv2DH5cpHP8UgRj9wdCcr2rWkJTgGJoo')
#             db.set_network(callback_query.from_user.id, 'TRC')
#             await state.set_state(Renting.rent_time)
#             await callback_query.message.answer_photo(photo=FSInputFile(card_photo_path),
#                                                       caption='🤖 <b>Введите сумму которую вы хотите пополнить на кошелек (в USDT, без точек и запятых):</b>',
#                                                       parse_mode='html', reply_markup=back_command_keyboard())
#
#     if callback_query.data == 'ERC':
#             await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
#             card_photo_path = 'fotos/bank_cards.jpg'
#             db.set_wallet(callback_query.from_user.id, '0x4B908f33111e968970bD4c5b1f6CE4014ad4F92E')
#             db.set_network(callback_query.from_user.id, 'ERC')
#             await state.set_state(Renting.rent_time)
#             await callback_query.message.answer_photo(photo=FSInputFile(card_photo_path),
#                                                       caption='🤖 <b>Введите сумму которую вы хотите пополнить на кошелек (в USDT, без точек и запятых):</b>',
#                                                       parse_mode='html', reply_markup=back_command_keyboard())
#
#
#
#     # проверка оплаты и подтверждение
#     try:
#             action, user_id = callback_query.data.split(':')
#             user_id = int(user_id)
#             rent = float(db.get_rent(user_id))
#             message_photo_path = 'fotos/message.jpg'
#             if action == 'success':
#                 db.set_user_wallet_make(user_id, rent)
#                 await bot.send_photo(photo=FSInputFile(message_photo_path), chat_id=user_id,
#                                      caption=f'✅ <b>Пополнение на кошелек прошло успешно!</b>\n\n'
#                                              f'💵 Кошелек: <b>{db.get_user_wallet(user_id)} USDT</b>', parse_mode='html',
#                                      reply_markup=back_command_keyboard())
#
#             if action == 'invalid':
#                 error_photo_path = 'fotos/error.jpg'
#                 await bot.answer_callback_query(callback_query.id)
#                 await bot.send_photo(photo=FSInputFile(error_photo_path), chat_id=user_id,
#                                      caption='❌ <b>Похоже что-то пошло не так. Возможно возникла проблема с обработкой данных.</b>\n\n'
#                                              '<i>Если вы уверены, что все данные верны обратитесь в поддержку: @pump_supporting_bot</i>',
#                                      parse_mode='html', reply_markup=back_command_keyboard())
#     except Exception:
#         pass









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



async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
