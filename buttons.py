from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

def admin_panel_buttons():
    buttons = [
        KeyboardButton(text="📜 Foydalanuvchilar ro'yxati"),
        KeyboardButton(text="Reklama joylash")
    ]
    return ReplyKeyboardMarkup(resize_keyboard=True).add(*buttons)








def main_menu():
    buttons = [
        KeyboardButton(text="⚠️ Shikoyat qilish ⚠️"),
        KeyboardButton(text="⚠️ Sayt orqali shikoyat qilish ⚠️"),
    ]
    return ReplyKeyboardMarkup(resize_keyboard=True).add(*buttons)

def get_contact_button():
    button = KeyboardButton(text="Telefon raqamni yuborish", request_contact=True)
    return ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button)

def tanlov():
    buttons = [
        KeyboardButton(text="📍 Lokatsiya yuboraman"),
        KeyboardButton(text="✍️ Matn yuboraman"),
    ]
    return ReplyKeyboardMarkup(resize_keyboard=True).add(*buttons)

def order_plant_buttons():
    buttons = [
        KeyboardButton(text="Ha"),
        KeyboardButton(text="Yo'q"),
    ]
    return ReplyKeyboardMarkup(resize_keyboard=True).add(*buttons)

def go_site():
    button = InlineKeyboardButton(text="Saytga o'tish", url="https://youtube.com")
    return InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button)





admin_panel_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Send Photo"), KeyboardButton(text="Send Video")],
        [KeyboardButton(text="Back to Main Menu")]
    ],
    resize_keyboard=True
)