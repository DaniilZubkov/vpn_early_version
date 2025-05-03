from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder



def main_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text='🌎 Подключиться', callback_data='connect_to_vpn'),
        InlineKeyboardButton(text='👤 Профиль', callback_data='view_profile'),
        InlineKeyboardButton(text='👨🏻‍🚀 Реферальная система', callback_data='referal_system'),
        InlineKeyboardButton(text='💳 Оплатить доступ', callback_data='pay_the_bot'),
        InlineKeyboardButton(text='💵 Пополнить кошелек', callback_data='bye_loot'),
    )
    builder.adjust(2, 1)
    return builder.as_markup()



def payment_keyboard1():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text='💳 Оплатить доступ', callback_data='pay_the_bot'),
        InlineKeyboardButton(text='💵 Пополнить кошелек', callback_data='bye_loot'),
        InlineKeyboardButton(
            text='🔙 Назад',
            callback_data='back_to_menu'
        )
    )
    builder.adjust(1)
    return builder.as_markup()



def profile_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text='💳 Оплатить доступ', callback_data='pay_the_bot'),
        InlineKeyboardButton(text='💵 Пополнить кошелек', callback_data='bye_loot'),
        InlineKeyboardButton(
            text='🔙 Назад',
            callback_data='back_to_menu'
        )
    )
    builder.adjust(1)
    return builder.as_markup()



def payment_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text='💳 1 месяц', callback_data='month'),
        InlineKeyboardButton(text='💳 6 месяцев', callback_data='halfyear'),
        InlineKeyboardButton(text='💳 1 год', callback_data='year'),
        InlineKeyboardButton(
            text='🔙 Назад',
            callback_data='back_to_menu'
        )
    )
    builder.adjust(3, 1)
    return builder.as_markup()



def pay_the_loot_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text='💵 Пополнить кошелек', callback_data='bye_loot'),
        InlineKeyboardButton(
            text='🔙 Назад',
            callback_data='back_to_menu'
        )
    )
    builder.adjust(1)
    return builder.as_markup()


def network1():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text='TON', callback_data='TON'),
        InlineKeyboardButton(text='TRC20', callback_data='TRC'),
        InlineKeyboardButton(text='ERC20', callback_data='ERC'),
        InlineKeyboardButton(
            text='🔙 Назад',
            callback_data='back_to_menu'
        )
    )
    builder.adjust(3, 1)
    return builder.as_markup()



def success_or_invalid():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text='✅ Успешно', callback_data='success'),
        InlineKeyboardButton(text='❌ Не успешно', callback_data='invalid')
    )
    return builder.as_markup()


def back_command_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text='🔙 Назад',
            callback_data='back_to_menu'
        )
    )
    return builder.as_markup()