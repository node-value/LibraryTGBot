import os, telebot
from telebot import types
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from g_drive_service import GoogleDriveService

BOT_TOKEN = os.environ.get('BOT_TOKEN')

starting_msgs = ['start', 'hello']
greatings = 'Hello, this is bot for getting accses to IT library of Nikita Vladimirov'

bot = telebot.TeleBot(BOT_TOKEN)

drive = GoogleDriveService()

def send_keyboard(buttons, msg):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1,one_time_keyboard=True)
    markup.add(*buttons)
    bot.reply_to(msg, "Please Choose Section", reply_markup=markup)

def send_document(d_path, msg):
    with open(d_path, 'rb') as doc:
        bot.send_document(msg.chat.id, doc)

@bot.message_handler(commands=starting_msgs)
def send_welcome(msg):
    bot.reply_to(msg, greatings)
    send_keyboard(drive.get_list_of_root_sections(), msg)

@bot.message_handler(func=lambda message: message.text in list(drive.section.keys()) + list(drive.title.keys()))
def handle_buttons(msg):
    pressed_button = msg.text
    if drive.is_section(pressed_button):
        send_keyboard(drive.get_list_of_content_in_section(pressed_button), msg)
    else:
        print("This is document you pressed: " + pressed_button)
        bot.reply_to(msg, 'Please wait, it will take a little time')
        path = drive.get_document(pressed_button)
        send_document(path, msg)
        os.remove(path)


bot.infinity_polling()