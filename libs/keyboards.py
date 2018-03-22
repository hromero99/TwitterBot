keyboard = types.InlineKeyboardMarkup()
keyboard.add(types.InlineKeyboardButton('RT', callback_data='rt'),
             types.InlineKeyboardButton('Fav', callback_data='fav'))