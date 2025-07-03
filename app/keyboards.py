from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='✅ Check', callback_data='check')],
        [InlineKeyboardButton(text='ℹ️ Info', callback_data='info'),
         InlineKeyboardButton(text='⚙️ Process', callback_data='process')],
        [InlineKeyboardButton(text='📸 Screen', callback_data='screen'),
         InlineKeyboardButton(text='📷 Camera', callback_data='camera')],
        [InlineKeyboardButton(text='🔊 Start recording', callback_data='start'),
         InlineKeyboardButton(text='🔊 Stop recording', callback_data='stop'),],
        [InlineKeyboardButton(text='🔒 Lock', callback_data='lock'),
         InlineKeyboardButton(text='🔓 Unlock', callback_data='unlock')]
    ]
)