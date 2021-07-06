from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

btnMain = KeyboardButton('⬅️ Главное меню')

# --- Main Menu ---
btnCrypto = KeyboardButton('Криптовалюты')
btnStock = KeyboardButton('Акции')
btnMoney = KeyboardButton('Курсы валют')
mainMenu = ReplyKeyboardMarkup(resize_keyboard = True).add(btnStock, btnCrypto, btnMoney)

# --- Other Menu ---
crXRP = KeyboardButton('XRP')
crBTC = KeyboardButton('BTC')
crETH = KeyboardButton('ETH')
CryptoMenu = ReplyKeyboardMarkup(resize_keyboard = True).add(crETH, crXRP, crBTC, btnMain)

#XRP menu
xrpStop = KeyboardButton ('Stop')
xrpOnce = KeyboardButton ('Посмотреть курс')
xrpCheck = KeyboardButton ('Следить за курсом')
xrpMenu = ReplyKeyboardMarkup(resize_keyboard = True).add(xrpOnce, xrpCheck, xrpStop, btnMain)
