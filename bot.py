import os
from dotenv import load_dotenv
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

load_dotenv()

TOKEN = os.getenv('TELEGRAM_API_TOKEN')
bot = telebot.TeleBot(TOKEN)

morse_table = {
    'А': '•—',   'Б': '— •••', 'В': '•——',  'Г': '—— •',  'Д': '— ••',  'Е': '•',    
    'Ё': '•',    'Ж': '•••—', 'З': '—— ••', 'И': '••',   'Й': '•———', 'К': '— •—',   
    'Л': '•— ••', 'М': '——',   'Н': '— •',   'О': '———',  'П': '•—— •', 'Р': '•— •',
    'С': '•••',  'Т': '—',    'У': '••—',  'Ф': '••— •', 'Х': '••••', 'Ц': '— •— •',
    'Ч': '——— •', 'Ш': '————',  'Щ': '—— •—', 'Ъ': '•—— •—','Ы': '— •——', 'Ь': '— ••—',
    'Э': '••— ••','Ю': '••—', 'Я': '', '1': '•————','2': '••———','3': '•••——',
    '4': '••••—', '5': '•••••','6': '— ••••','7': '—— •••','8': '——— ••','9': '———— •','0': '—————'
}

reverse_morse_table = {value: key for key, value in morse_table.items()}

@bot.message_handler(commands=['start'])
def welcome(message):
    markup = InlineKeyboardMarkup()
    button_learn = InlineKeyboardButton("Учить", callback_data='learn')
    button_train = InlineKeyboardButton("Тренироваться", callback_data='train')
    markup.add(button_learn, button_train)
    bot.send_message(message.chat.id, "Привет! Этот бот поможет тебе выучить азбуку Морзе.", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == 'learn':
        learn(call.message)
    elif call.data == 'train':
        train(call.message)

def learn(message):
    full_table = "\n".join(f"{char}: {code}" for char, code in sorted(morse_table.items()))
    bot.send_message(message.chat.id, f"Вот полная таблица Азбуки Морзе:\n\n{full_table}")

def train(message):
    markup = InlineKeyboardMarkup()
    ranges = ["А-И", "Й-Я", "А-Я", "Цифры", "Буквы и цифры", "Свой диапазон"]
    buttons = [InlineKeyboardButton(text=rng, callback_data=f'train_{rng}') for rng in ranges]
    markup.add(*buttons)
    bot.send_message(message.chat.id, "Выбери диапазон:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('train_'))
def select_range(call):
    selected_range = call.data.split('_')[1]
    if selected_range == "Свой диапазон":
        bot.send_message(call.message.chat.id, "Напиши диапазон букв (пример: А-И)")
    else:
        train_range(selected_range, call.message)

def train_range(rng, message):
    chars = []
    if rng == "А-И": chars.extend(list("АБВГДЕЁЖЗИ"))
    elif rng == "Й-Я": chars.extend(list("ЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"))
    elif rng == "А-Я": chars.extend(list("АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"))
    elif rng == "Цифры": chars.extend(list("1234567890"))
    elif rng == "Буквы и цифры": chars.extend(list("АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ1234567890"))

    random_char = chars.pop()
    answer = reverse_morse_table[morse_table[random_char]]
    user_input = input("Ваш ответ:")
    if user_input.upper() == answer:
        bot.send_message(message.chat.id, "Правильный ответ! Идем дальше.")
    else:
        bot.send_message(message.chat.id, f"Ответ неверный(( Правильный ответ был: {answer}.")

bot.polling(non_stop=True)
