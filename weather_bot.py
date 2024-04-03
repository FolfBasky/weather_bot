import telebot
import requests

weather_key = '456d34629ab92f038d044cefbe858463'

# Ваш токен, который вы получили при регистрации бота
TOKEN = '6066420729:AAHvZPs9ZSUHxGYVHum1MLIgdDPo6Hjw8go'
bot = telebot.TeleBot(TOKEN)

# Кнопки для выбора действий
markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
button1 = telebot.types.KeyboardButton('Получить погоду 🌤️')
button2 = telebot.types.KeyboardButton('О проекте ℹ️')
markup.add(button1, button2)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.reply_to(message, "Привет! Я бот, который может показать погоду и рассказать о проекте. Выбери один из вариантов в меню ниже:", reply_markup=markup)

# Обработчик кнопки "Получить погоду"
@bot.message_handler(func=lambda message: message.text == 'Получить погоду 🌤️')
def weather_handler(message):
    # Запрашиваем у пользователя город
    bot.send_message(message.chat.id, "Введите название города:")
    # Сохраняем контекст пользователя, чтобы в следующем сообщении понимать, что он ждет ответа на запрос города
    bot.register_next_step_handler(message, get_weather)

# Функция для получения погоды после запроса города у пользователя
def get_weather(message):
    city = message.text
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_key}'
    response = requests.get(url)
    weather_data = response.json()

    # Обработка ответа от API и формирование сообщения для пользователя
    if response.status_code == 200:
        temperature = round(weather_data['main']['temp'] - 273.15)
        feels_like = round(weather_data['main']['feels_like'] - 273.15)
        min_temperature = round(weather_data['main']['temp_min'] - 273.15)
        max_temperature = round(weather_data['main']['temp_max'] - 273.15)
        weather_description = weather_data['weather'][0]['description'].capitalize()
        icon = weather_data['weather'][0]['icon']
        emoji = ''
        if '01' in icon:
            emoji = '☀️'
        elif '02' in icon:
            emoji = '🌤️'
        elif '03' in icon or '04' in icon:
            emoji = '☁️'
        elif '09' in icon:
            emoji = '🌧️'
        elif '10' in icon:
            emoji = '🌦️'
        elif '11' in icon:
            emoji = '⛈️'
        elif '13' in icon:
            emoji = '❄️'
        elif '50' in icon:
            emoji = '🌫️'
        message_text = f'Текущая погода в городе {city} :\n\nТемпература: {temperature}°C\nОщущается как: {feels_like}°C\nМинимальная температура: {min_temperature}°C\nМаксимальная температура: {max_temperature}°C\nОписание погоды: {weather_description}{emoji}'
        bot.send_message(message.chat.id, message_text)
    else:
        bot.send_message(message.chat.id, 'Ошибка при получении данных о погоде. Попробуйте позже.')

    
# Обработчик кнопки "О проекте"
@bot.message_handler(func=lambda message: message.text == 'О проекте ℹ️')
def about_handler(message):
    message_text = 'Этот проект создан с помощью Telebot и API для погоды от OpenWeatherMap.'
    bot.reply_to(message, message_text)

# Запуск бота
bot.polling()