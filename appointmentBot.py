import os
from dotenv import load_dotenv
import telebot
import requests
from datetime import datetime, timedelta
import pytz
import time
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
# Function to get daily horoscope
def get_daily_horoscope(sign: str, day: str) -> dict:
    """Get daily horoscope for a zodiac sign.
    Keyword arguments:
    sign:str - Zodiac sign
    day:str - Date in format (YYYY-MM-DD) OR TODAY OR TOMORROW OR YESTERDAY
    Return:dict - JSON data
    """
    url = "https://horoscope-app-api.vercel.app/api/v1/get-horoscope/daily"
    params = {"sign": sign, "day": day}
    response = requests.get(url, params)
    response = response.json()
    return response

# Load environment variables from .env file
load_dotenv()
geolocator = Nominatim(user_agent="telegram_bot")
# Dictionary to store user timezones
user_timezones = {}
# Get the API key from the environment
BOT_TOKEN = os.getenv("TELEGRAM_API_KEY")

# Initialize the bot
bot = telebot.TeleBot(BOT_TOKEN)

# Dictionary to store appointments
appointments = {}

# Command handlers
@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    greeting_message = "Welcome to Odd Tech! How can I assist you today?"
    options_message = "Here are some options you can try:\n" \
                      "/horoscope - Get your daily horoscope\n" \
                      "/book_appointment - Book an appointment\n" \
                      "/my_time - Get current time in your timezone\n"
    bot.send_message(message.chat.id, greeting_message)
    bot.send_message(message.chat.id, options_message)

@bot.message_handler(commands=['horoscope'])
def sign_handler(message):
    text = "What's your zodiac sign?\nChoose one: *Aries*, *Taurus*, *Gemini*, *Cancer,* *Leo*, *Virgo*, *Libra*, *Scorpio*, *Sagittarius*, *Capricorn*, *Aquarius*, and *Pisces*."
    sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg, day_handler)

def day_handler(message):
    sign = message.text
    text = "What day do you want to know?\nChoose one: *TODAY*, *TOMORROW*, *YESTERDAY*, or a date in format YYYY-MM-DD."
    sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg, fetch_horoscope, sign.capitalize())

def fetch_horoscope(message, sign):
    day = message.text
    horoscope = get_daily_horoscope(sign, day)
    data = horoscope["data"]
    if horoscope["status"] == 200:
        horoscope_message = f'*Horoscope:* {data["horoscope_data"]}\n*Sign:* {sign}\n*Day:* {data["date"]}'
        bot.send_message(message.chat.id, horoscope_message, parse_mode="Markdown")
    else:
        bot.send_message(message.chat.id, "Sorry, I couldn't fetch the horoscope for you at the moment.")

# Appointment booking handler
@bot.message_handler(commands=['book_appointment'])
def book_appointment(message):
    bot.send_message(message.chat.id, "Please enter the date for your appointment in the format YYYY-MM-DD (e.g., 2024-03-28)")
    bot.register_next_step_handler(message, process_date)

def process_date(message):
    try:
        # Parse the date entered by the user
        appointment_date = datetime.strptime(message.text, "%Y-%m-%d")
        # Ask for the time and provide a sample format
        bot.send_message(message.chat.id, "Please enter the time for your appointment in the format HH:MM (e.g., 14:30)")
        bot.register_next_step_handler(message, process_time, appointment_date)
    except ValueError:
        bot.send_message(message.chat.id, "Invalid date format! Please use the format YYYY-MM-DD (e.g., 2024-03-28)")

def process_time(message, appointment_date):
    try:
        # Parse the time entered by the user
        appointment_time = datetime.strptime(message.text, "%H:%M").time()
        # Combine the date and time to create the appointment datetime
        appointment_datetime = datetime.combine(appointment_date, appointment_time)
        # Store the appointment in the dictionary
        appointments[message.chat.id] = appointment_datetime
        bot.send_message(message.chat.id, f"Appointment booked for {appointment_datetime.strftime('%Y-%m-%d %H:%M')}")
    except ValueError:
        bot.send_message(message.chat.id, "Invalid time format! Please use the format HH:MM (e.g., 14:30)")

@bot.message_handler(commands=['my_time'])
def get_user_time(message):
    user_id = message.chat.id
    if user_id in user_timezones:
        user_timezone = user_timezones[user_id]
        try:
            tz = pytz.timezone(user_timezone)
            current_time = datetime.now(tz)
            time_message = f"The current time in your timezone ({user_timezone}) is: {current_time.strftime('%Y-%m-%d %H:%M:%S')}"
            bot.send_message(message.chat.id, time_message)
        except pytz.UnknownTimeZoneError:
            bot.send_message(message.chat.id, "Sorry, I couldn't determine your timezone.")
    else:
        bot.send_message(message.chat.id, "Please set your city using /set_city command first.")

@bot.message_handler(commands=['set_city'])
def set_city(message):
    bot.send_message(message.chat.id, "Please enter your city name:")
    bot.register_next_step_handler(message, save_city)

def save_city(message):
    try:
        location = geolocator.geocode(message.text)
        if location:
            obj = TimezoneFinder() 
            timezone_str = obj.timezone_at(lng=location.longitude, lat=location.latitude) 
            if timezone_str:
                user_timezones[message.chat.id] = timezone_str
                bot.send_message(message.chat.id, f"Your timezone has been set to {timezone_str}")
            else:
                bot.send_message(message.chat.id, "Timezone not found for the given city.")
        else:
            bot.send_message(message.chat.id, "City not found. Please enter a valid city name.")
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, "An error occurred while processing your request.")



# Appointment reminder handler
def check_reminders():
    current_time = datetime.now()
    print(current_time)
    for chat_id, appointment_datetime in appointments.items():
        #adjust reminder time 
        if appointment_datetime - timedelta(hours=1) <= current_time <= appointment_datetime:
            bot.send_message(chat_id, "Reminder: Your appointment is in 1 hour!")

# Polling for reminders
def polling_reminders():
    while True:
        try:
            check_reminders()
            bot.polling(none_stop=True)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(15)

# Start polling for reminders
polling_reminders()