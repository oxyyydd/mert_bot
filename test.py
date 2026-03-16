import telebot
from telebot import types
import re

# Твой токен
TOKEN = '8616582923:AAE5PJKkK7LdiL4xBPfrz4SCKfmefq0b0nw'
bot = telebot.TeleBot(TOKEN)

user_progress = {}


WORDS = {
    'start': ['los get\'s', 'los get s', 'los gehts', 'los geht es', 'los', 'let’s go', 'lets go', 'поехали'],
    'cafe': ['karte', 'geburtstagskarte', 'открытка', 'grusskarte', 'postkarte'],
    'call': ['torte', 'geburtstagstorte', 'kuchen', 'cheesecake', 'торт'],
    'sweater': ['pulli', 'pullover', 'sweater', 'oberteil', 'longsleeve', 'свитер']
}

def get_hint_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(types.KeyboardButton('Tipp 💡'))
    return markup

def clean_text(text):
    return re.sub(r'[^\w\s\']', '', text.lower()).strip()

@bot.message_handler(commands=['start'])
def start_cmd(message):
    user_progress[message.chat.id] = 'waiting_start'
    bot.send_message(message.chat.id, 'Guten Morgen, kotjenok. Wie schön, dass es dich gibt! Ich habe etwas für dich vorbereitet.\nSteh auf, putz dir die Zähne und dann treffen wir uns um 12:00 Uhr am Bahnhof.')

@bot.message_handler(func=lambda message: True)
def game_logic(message):
    chat_id = message.chat.id
    raw_text = message.text.lower().strip()
    text = clean_text(message.text)
    step = user_progress.get(chat_id, 'waiting_start')

    # --- ЛОГИКА ПОДСКАЗОК ---
    if 'tipp' in raw_text or 'подсказка' in raw_text:
        if step == 'cafe':
            # ЗАМЕНИ ЭТУ ССЫЛКУ НА РЕАЛЬНУЮ С GOOGLE MAPS
            bot.send_message(chat_id, 'Hier ist der Standort vom Café: https://maps.app.goo.gl/CU7TauyZZBs6TerK8?g_st=it')
        elif step == 'call':
            try:
                with open('photo_2026-03-12_14-40-27.jpg', 'rb') as photo:
                    bot.send_photo(chat_id, photo, caption='Hier ist dein Tipp — ruf diese Person an!')
            except FileNotFoundError:
                bot.send_message(chat_id, 'Tipp: Ruf die Person von der Karte an!')
        else:
            bot.send_message(chat_id, 'An dieser Stelle gibt es keine Tipps mehr, streng dein Köpfchen an! 😉')
        return

    # --- ЛОГИКА ЭТАПОВ ---

    # ЭТАП 1: Встреча -> Кафе
    if step == 'waiting_start' and text in WORDS['start']:
        user_progress[chat_id] = 'cafe'
        bot.send_message(chat_id, 'Ich wünsche dir in deinem neuen Lebensjahr weniger von solchen unangenehmen Momenten. Und wenn sie doch passieren, werden wir bestimmt irgendwann darüber lachen.\nJetzt halte Kurs auf das Café, in dem dich die nette Dame, glückliche Mutter von zwei kleinen Engeln, vor dem ganzen Personal angeschrien hat.\n\nDort warten deine Freunde auf dich. Falls du sie nicht sofort findest, frag einfach jemanden an der Kasse.\nSchreib mir, was du da gefunden hast.', reply_markup=get_hint_keyboard())

    # ЭТАП 2: Кафе -> Звонок
    elif step == 'cafe' and text in WORDS['cafe']:
        user_progress[chat_id] = 'call'
        bot.send_message(chat_id, 'Dein weiterer Weg liegt im Nebel der Galaxis…\nNur Meister Yoda kennt die nächste Etappe deiner Reise.\n\nAber keine Sorge: Anders als Luke musst du dafür nicht auf einen anderen Planeten fliegen.\nRuf ihn einfach an – er wird dir den nächsten Schritt verraten.', reply_markup=get_hint_keyboard())

    # ЭТАП 3: Звонок -> Торт
    elif step == 'call' and text in WORDS['call']:
        user_progress[chat_id] = 'sweater'
        bot.send_message(chat_id, 'Guten Appetit! Ich hoffe, der Kuchen kommt deinen Vorstellungen wenigstens ein kleines bisschen nahe.\n\nUnd jetzt geh nach oben (du kannst die Torte gern mitnehmen).\nAuf dem Sofa findest du den nächsten Hinweis.\nSchreib mir das Wort, sobald du es entdeckt hast.')

    # ЭТАП 4: Торт -> Финал
    elif step == 'sweater' and text in WORDS['sweater']:
        user_progress[chat_id] = 'home'
        bot.send_message(chat_id, 'Danke für deine Geduld – du hast das super gemacht!\nNur noch ein letzter Schritt.\n\nDein Hauptgeschenk wartet dort auf dich, wo auch deine frische, saubere Wäsche auf dich wartet. 😅', reply_markup=types.ReplyKeyboardRemove())

    else:
        bot.send_message(chat_id, 'Ich verstehe dich nicht ganz. Probier es nochmal oder nutze den Tipp-Button.')

bot.polling(none_stop=True)
