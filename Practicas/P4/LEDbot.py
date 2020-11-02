import telebot
from gpiozero import LED

led = LED(26)

API_TOKEN = '1391144634:AAHEamkwuK8d0Q-oYpEPn59fiBXzGGkq-uA'

bot = telebot.TeleBot(API_TOKEN)

# Handle '/on'
@bot.message_handler(commands=['on'])
def encender(message):
	led.on()
	bot.reply_to(message, """\
Se hizo la luz!!\
""")

#Handle '/off'
@bot.message_handler(commands=['off'])
def encender(message):
	led.off()
	bot.reply_to(message, """\
Se murió :(\
""")

bot.polling()