import os, telebot
from telebot import types
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from g_drive_service import GoogleDriveService
from constants import Constants

bot   = telebot.TeleBot(Constants.BOT_TOKEN)
drive = GoogleDriveService()
queue = []

def send_keyboard(buttons, msg):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1,one_time_keyboard=True)
    markup.add(*buttons)
    bot.reply_to(msg, Constants.CHOOSE_SECTION, reply_markup=markup)

def send_document(d_path, msg):
    with open(d_path, 'rb') as doc:
        bot.send_document(msg.chat.id, doc)

@bot.message_handler(commands=Constants.START_MSGS)
def send_welcome(msg):
    bot.reply_to(msg, Constants.GREATINGS)
    buttons = drive.get_list_of_root_sections()
    send_keyboard(buttons, msg)
    queue.append(buttons)

@bot.message_handler(func=lambda message: message.text in list(drive.section.keys()))
def handle_section_buttons(msg):
    pressed_button = msg.text
    buttons = drive.get_list_of_content_in_section(pressed_button) + [Constants.BACK_BTN]
    send_keyboard(buttons, msg)
    queue.append(buttons)

@bot.message_handler(func=lambda message: message.text in list(drive.title.keys()))
def handle_title_buttons(msg):
    pressed_button = msg.text
    bot.reply_to(msg, Constants.PLS_WAIT)
    path = drive.get_document(pressed_button)
    send_document(path, msg)
    os.remove(path)

@bot.message_handler(func=lambda message: message.text == Constants.BACK_BTN)
def handle_back_button(msg):
    queue.pop()
    send_keyboard(queue[-1], msg)

bot.infinity_polling()