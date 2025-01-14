from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

main_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton('🌎 Подключиться', callback_data='connect_to_vpn'), InlineKeyboardButton('👤 Профиль', callback_data='view_profile')],
    [InlineKeyboardButton('👨🏻‍🚀 Реферальная система', callback_data='referal_system')],
    [InlineKeyboardButton('💳 Оплатить доступ', callback_data='pay_the_bot')]
])

payment_keyboard1 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton('💳 Оплатить доступ', callback_data='pay_the_bot')]
])

profile_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton('💳 Оплатить доступ', callback_data='pay_the_bot')],
    [InlineKeyboardButton('💵 Пополнить кошелек', callback_data='bye_loot')],
])

payment_keyboard = InlineKeyboardMarkup(inline_keyboard=[(
   InlineKeyboardButton(text='💳 1 месяц', callback_data='month'),
    InlineKeyboardButton(text='💳 6 месяцев', callback_data='halfyear'),
    InlineKeyboardButton(text='💳 1 год', callback_data='year')
)], row_width=1)

pay_the_loot_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton('💵 Пополнить кошелек', callback_data='bye_loot')]
])

network1 = InlineKeyboardMarkup(inline_keyboard=[(
    InlineKeyboardButton(text='TON', callback_data='TON'),
    InlineKeyboardButton(text='TRC20', callback_data='TRC'),
    InlineKeyboardButton(text='ERC20', callback_data='ERC')
)])

succes_or_invalid = InlineKeyboardMarkup(inline_keyboard=[(
    InlineKeyboardButton(text='✅Успешно', callback_data='success'),
    InlineKeyboardButton(text='❌Не успешно', callback_data='invalid')
)])