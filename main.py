from aiogram import Bot, Dispatcher, types, executor
from states import Registration, LocationStates, AdminPanelState
import logging
from aiogram.dispatcher import FSMContext
from buttons import *
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from database import Database
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton

logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()

API_TOKEN = "6827097914:AAFIFkQnl4lnYiyrnM6I875Q50P92fmsr-0"

bot = Bot(token=API_TOKEN, parse_mode='html')

dp = Dispatcher(bot, storage=storage)

db = Database()

ADMIN_CHAT_IDS = ["7149602547", "5440072681"]  


async def on_startup(dispatcher):
    for admin_id in ADMIN_CHAT_IDS:
        await bot.send_message(admin_id, "Bot started successfully!")

async def on_shutdown(dispatcher):
    for admin_id in ADMIN_CHAT_IDS:
        await bot.send_message(admin_id, "Bot is shutting down. Goodbye!")


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    user = db.get_user(user_id)
    
    if user:
        full_name = message.from_user.full_name
        await message.answer(f"👋 Salom <b>{full_name}</b> Botimizga xush kelibsiz!", reply_markup=main_menu(), parse_mode="HTML")
    else:
        full_name = message.from_user.full_name
        await message.answer(f"Salom {full_name}. Botimizga xush kelibsiz!")
        await message.answer("⚠️ Botimizdan to'liq foydalanish uchun registratsiyadan o'tishingiz kerak ⚠️")
        await message.answer("👤  Ismingizni kiriting: ")
        await Registration.waiting_for_name.set()


@dp.message_handler(state=Registration.waiting_for_name, content_types=types.ContentTypes.TEXT)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['full_name'] = message.text
    await message.answer("☎️ Telefon raqamingizni yuboring:", reply_markup=get_contact_button())
    await Registration.waiting_for_phone_number.set()


@dp.message_handler(state=Registration.waiting_for_phone_number, content_types=types.ContentTypes.CONTACT)
async def process_phone_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone_number'] = message.contact.phone_number
        user_id = message.from_user.id

        # Save to SQLite3
        try:
            db.add_user(user_id, data['full_name'], data['phone_number'])
            await message.answer("🥳🥳 Registratsiyadan muvaffaqiyatli o'tdingiz!" , reply_markup=main_menu())
        except Exception as e:
            await message.answer(f"Xatolik yuz berdi: {str(e)}")

    await state.finish()


@dp.message_handler(text="⚠️ Shikoyat qilish ⚠️")
async def chiqindi_handler(message: types.Message):
    user_id = message.from_user.id
    user = db.get_user(user_id)
    
    if user:
        await message.answer("Lokatsiya yuboring. Matn ko'rinishidami yoki Lokatsiya ko'rinishidami?", reply_markup=tanlov())  


@dp.message_handler(text="📍 Lokatsiya yuboraman")
async def send_location_handler(message: types.Message):
    await message.answer("Iltimos, lokatsiyangizni yuboring.", reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton("Lokatsiyani yuborish", request_location=True)))
    await LocationStates.waiting_for_location.set()


@dp.message_handler(content_types=types.ContentTypes.LOCATION, state=LocationStates.waiting_for_location)
async def receive_location(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['location'] = message.location
    await message.answer("🖼️ Shikoyat qilayotaga joyni rasmini yugoring: ", reply_markup=ReplyKeyboardRemove())
    await LocationStates.waiting_for_image.set()


@dp.message_handler(content_types=types.ContentTypes.PHOTO, state=LocationStates.waiting_for_image)
async def receive_image(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['image'] = message.photo[-1].file_id
        user_id = message.from_user.id
        user = db.get_user(user_id)

    await message.answer("Ma'sullar tez orada habardor etiladi !", reply_markup=main_menu())
    await state.finish()

@dp.message_handler(text="✍️ Matn yuboraman")
async def send_matn_handler(message: types.Message):
    await message.answer("Lokatsiyani matn ko'rinishida yuboring:", reply_markup=ReplyKeyboardRemove())
    await LocationStates.waiting_for_text_location.set()

@dp.message_handler(state=LocationStates.waiting_for_text_location, content_types=types.ContentTypes.TEXT)
async def receive_text_location(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text_location'] = message.text
    await message.answer("Rasm yuboring.")
    await LocationStates.waiting_for_image_text.set()

@dp.message_handler(content_types=types.ContentTypes.PHOTO, state=LocationStates.waiting_for_image_text)
async def receive_image_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['image'] = message.photo[-1].file_id
        user_id = message.from_user.id
        user = db.get_user(user_id)

    await message.answer("Ma'sullar tez orada habardor etiladi", reply_markup=main_menu())    
    await state.finish()




    # Send a message to the admins
    for admin_id in ADMIN_CHAT_IDS:
        await bot.send_message(admin_id, f"Foydalanuvchi {user[2]} ({user[3]}) quyidagi joyda chiqindilarni tashlagan:\n\nLokatsiya: {data['text_location']}\n\nRasm:", parse_mode="HTML")
        await bot.send_photo(admin_id, photo=data['image'])

@dp.message_handler(text="⚠️ Sayt orqali shikoyat qilish ⚠️")
async def buyurtma_handler(message: types.Message):
    user_id = message.from_user.id
    user = db.get_user(user_id)

    if user:
        await message.answer("""Saytga o'tish uchun 👇BOSING👇""", reply_markup=go_site())
        







# admin panel










@dp.message_handler(commands=['admin'])
async def admin_panel_handler(message: types.Message):
    user_id = message.from_user.id
    if str(user_id) in ADMIN_CHAT_IDS:
        await message.answer("Admin paneliga xush kelibsiz!", reply_markup=admin_panel_buttons())
    else:
        await message.answer("Sizda ushbu bo'limga kirish huquqi yo'q!")


@dp.message_handler(text="📜 Foydalanuvchilar ro'yxati")
async def users_list_handler(message: types.Message):
    user_id = message.from_user.id
    if str(user_id) in ADMIN_CHAT_IDS:
        users = db.get_all_users()
        user_list = "\n".join([f"{user[1]} ({user[2]})" for user in users])
        await message.answer(f"Foydalanuvchilar ro'yxati:\n{user_list}")
    else:
        await message.answer("Sizda ushbu bo'limga kirish huquqi yo'q!")






        
@dp.message_handler(text="Reklama joylash")
async def myadminpanel(message: types.Message):
    await message.answer("Reklama usulini tanlang: ", reply_markup=admin_panel_keyboard)
    await AdminPanelState.waiting_for_media_choice.set()


@dp.message_handler(text="Back to Main Menu")
async def back_to_main_menu_to_admin(message:types.Message):
    await message.answer("Main Menu: ", reply_markup=main_menu)

@dp.message_handler(state=AdminPanelState.waiting_for_media_choice, text="Send Photo")
async def admin_panel_send_photo(message: types.Message):
    await message.answer("Rasm yuboring:")
    await AdminPanelState.waiting_for_image.set()




@dp.message_handler(state=AdminPanelState.waiting_for_image, content_types=types.ContentType.PHOTO)
async def admin_panel_image(message: types.Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    await state.update_data(photo_id=photo_id)
    await message.answer("Rasm qabul qilindi. Caption yuboring: ")
    await AdminPanelState.waiting_for_caption.set()




@dp.message_handler(state=AdminPanelState.waiting_for_media_choice, text="Send Video")
async def admin_panel_send_video(message: types.Message):
    await message.answer("Video yuboring:")
    await AdminPanelState.waiting_for_video.set()


@dp.message_handler(state=AdminPanelState.waiting_for_video, content_types=types.ContentType.VIDEO)
async def admin_panel_video(message: types.Message, state: FSMContext):
    video_id = message.video.file_id
    await state.update_data(video_id=video_id)
    await message.answer("Video qabul qilindi. Caption yuboring: ")
    await AdminPanelState.waiting_for_caption.set()


@dp.message_handler(state=AdminPanelState.waiting_for_caption)
async def admin_panel_caption(message: types.Message, state: FSMContext):
    caption = message.text
    data = await state.get_data()

    # Barcha foydalanuvchilarni olish
    chat_ids = db.get_all_chat_ids()
    
    # Rasm yoki video yuborish
    if 'photo_id' in data:
        photo_id = data['photo_id']
        for chat_id in chat_ids:
            try:
                await bot.send_photo(chat_id=chat_id, photo=photo_id, caption=caption)
            except Exception as e:
                logging.error(f"Failed to send photo to {chat_id}: {e}")
    elif 'video_id' in data:
        video_id = data['video_id']
        for chat_id in chat_ids:
            try:
                await bot.send_video(chat_id=chat_id, video=video_id, caption=caption)
            except Exception as e:
                logging.error(f"Failed to send video to {chat_id}: {e}")

    await message.answer("Media va caption barcha foydalanuvchilarga yuborildi.", reply_markup=admin_panel_keyboard)
    await AdminPanelState.waiting_for_media_choice.set()





@dp.message_handler(state=AdminPanelState.waiting_for_image, content_types=types.ContentType.PHOTO)
async def admin_panel_image(message: types.Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    await state.update_data(photo_id=photo_id)
    await message.answer("Rasm qabul qilindi. Caption yuboring: ")
    await AdminPanelState.waiting_for_caption.set()

@dp.message_handler(state=AdminPanelState.waiting_for_caption)
async def admin_panel_caption(message: types.Message, state: FSMContext):
    caption = message.text
    data = await state.get_data()
    photo_id = data['photo_id']
    
    # Barcha foydalanuvchilarni olish
    chat_ids = db.get_all_chat_ids()
    
    # Har bir foydalanuvchiga rasm va caption yuborish
    for chat_id in chat_ids:
        try:
            await bot.send_photo(chat_id=chat_id, photo=photo_id, caption=caption)
        except Exception as e:
            logging.error(f"Failed to send photo to {chat_id}: {e}")
    
    await message.answer("Rasm va caption barcha foydalanuvchilarga yuborildi.")
    await state.finish()








if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)

    