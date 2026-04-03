import telebot
from telebot import types
import re

TOKEN = '8616582923:AAE5PJKkK7LdiL4xBPfrz4SCKfmefq0b0nw'
bot = telebot.TeleBot(TOKEN)

user_progress = {}

MAP_LINK = "https://maps.app.goo.gl?link=https://www.google.com/maps/@/data%3D!4m5!7m4!1m2!1s103222502778246472204!2sChZ5cWVncUhrY2c3WmJieDRiUlFncGVBEggHBk6QgS__Pg%253D%253D!2e2?hl%3Dru&apn=com.google.android.apps.maps&amv=949000000&ius=comgooglemapsurl&isi=585027354&ct=location-sharing-fdl&mt=8&pt=9008&ibi=com.google.Azimuth&ibi=com.google.Azimuth.MessagesExtension&ibi=com.google.Bzimuth&ibi=com.google.Bzimuth.MessagesExtension&ibi=com.google.Czimuth&ibi=com.google.Czimuth.MessagesExtension&ibi=com.google.Dzimuth&ibi=com.google.Dzimuth.MessagesExtension&ibi=com.google.Maps&ibi=com.google.Maps.MessagesExtension&ibi=com.google.Rzimuth&ibi=com.google.Rzimuth.MessagesExtension&afl=https://www.google.com/maps/@/data%3D!4m5!7m4!1m2!1s103222502778246472204!2sChZ5cWVncUhrY2c3WmJieDRiUlFncGVBEggHBk6QgS__Pg%253D%253D!2e2?hl%3Dru&ifl=https://www.google.com/maps/@/data%3D!4m5!7m4!1m2!1s103222502778246472204!2sChZ5cWVncUhrY2c3WmJieDRiUlFncGVBEggHBk6QgS__Pg%253D%253D!2e2?hl%3Dru"

WORDS = {
    'start': ['los geht', 'los', 'lets go'],
    'sweater': ['pulli', 'pullover', 'sweater', 'oberteil', 'longsleeve'],
    'karte': ['karte', 'geburtstagskarte'],
    'call': ['torte', 'geburtstagstorte', 'kuchen', 'cheesecake'],
    'matte': ['matte', 'yoga matte', 'yogamatte']
}

def get_hint_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(types.KeyboardButton('Tipp 💡'))
    return markup

def clean_text(text):
    return re.sub(r'[^\w\s]', '', text.lower()).strip()

def match(words, text):
    return any(word in text for word in words)

@bot.message_handler(commands=['start'])
def start_cmd(message):
    user_progress[message.chat.id] = 'waiting_start'
    bot.send_message(
        message.chat.id,
        'Guten Morgen, kotjenok. Wie schön, dass es dich gibt! Ich habe etwas für dich vorbereitet.\n'
        'Steh auf, putz dir die Zähne und dann treffen wir uns um 12:30 Uhr am Bahnhof.'
    )

@bot.message_handler(func=lambda message: True)
def game_logic(message):
    chat_id = message.chat.id
    raw_text = message.text.lower().strip()
    text = clean_text(message.text)
    step = user_progress.get(chat_id, 'waiting_start')

    # ПОДСКАЗКИ
    if 'tipp' in raw_text:
        if step == 'sweater':
            bot.send_message(
                chat_id,
                f'Hier ist dein Hinweis: <a href="{MAP_LINK}">Ort auf Google Maps ansehen</a>\n(klicke auf den Link)',
                parse_mode='HTML'
            )
        elif step == 'call':
            try:
                with open('photo_2026-03-12_14-40-27.jpg', 'rb') as photo:
                    bot.send_photo(
                        chat_id,
                        photo,
                        caption='Schade, mein Mann ist Loch 🕳️. Hast du Fredi nicht erkannt?'
                    )
            except:
                bot.send_message(chat_id, 'Tipp: Ruf die richtige Person an 😉')
        else:
            bot.send_message(chat_id, 'Hier gibt es keinen Tipp mehr 😏')
        return

    # ЭТАПЫ

    if step == 'waiting_start' and match(WORDS['start'], text):
        user_progress[chat_id] = 'sweater'
        bot.send_message(chat_id,
            'Ich bin dankbar für jede Minute mit dir und auch einfach sehr glücklich, dass wir uns haben.\n\n'
            'Und das hätte alles auch ganz anders laufen können…\n\n'
            'Geh zu dem Ort, an dem ich damals fast alles kaputt gemacht hätte.\n'
            'Schreib mir, was du dort findest.',
            reply_markup=get_hint_keyboard()
        )

    elif step == 'sweater' and match(WORDS['sweater'], text):
        user_progress[chat_id] = 'karte'
        bot.send_message(chat_id,
            '„Im düsteren Dunkel der fernen Zukunft gibt es nur Krieg…“ – aber in unserer Zeit gibt es wichtigere Probleme…\n'
            'zum Beispiel ein gemeinsames Hobby zu finden.\n\n'
            'Vielleicht finden wir irgendwann wirklich eins, aber das war es wohl eher nicht.\n\n'
            'Geh dorthin, wo Igor geboren wurde – aber sei vorsichtig, dort ist von 13:00 bis 13:30 Mittagspause.\n\n'
            'Schreib mir, was du dort findest.',
            reply_markup=get_hint_keyboard()
        )

    elif step == 'karte' and match(WORDS['karte'], text):
        user_progress[chat_id] = 'call'
        bot.send_message(chat_id,
            'Dein weiterer Weg liegt im Nebel der Galaxis…\n\n'
            'Nur Meister Yoda kennt die nächste Etappe deiner Reise.\n\n'
            'Ruf ihn einfach an – er wird dir den nächsten Schritt verraten.',
            reply_markup=get_hint_keyboard()
        )

    elif step == 'call' and match(WORDS['call'], text):
        user_progress[chat_id] = 'cake'
        bot.send_message(chat_id,
            'Guten Appetit! Ich hoffe, der Kuchen kommt deinen Vorstellungen wenigstens ein kleines bisschen nahe.\n\n'
            'Und jetzt: geh nach oben (du darfst die Torte natürlich mitnehmen).\n\n'
            'Auf dem Sofa wartet der nächste Hinweis auf dich.\n'
            'Schreib mir das Wort, sobald du es entdeckt hast.'
        )

    elif step == 'cake' and match(WORDS['matte'], text):
        user_progress[chat_id] = 'home'
        bot.send_message(chat_id,
            'Danke für deine Geduld – du hast das wirklich richtig gut gemacht.\n\n'
            'Jetzt fehlt nur noch ein letzter Schritt…\n\n'
            'Dein Hauptgeschenk wartet genau dort auf dich, wo auch deine frische, saubere Wäsche auf dich wartet 😏',
            reply_markup=types.ReplyKeyboardRemove()
        )

    else:
        bot.send_message(chat_id, 'Ich verstehe dich nicht ganz. Probier es nochmal oder nutze den Tipp-Button.'

if __name__ == "__main__":
    while True:
        try:
            print("Бот запущен...")
            bot.polling(none_stop=True, timeout=60)
        except Exception as e:
            print("Ошибка:", e)