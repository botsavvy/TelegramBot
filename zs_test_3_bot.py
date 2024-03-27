import telebot
import datetime
import pytz
from geopy.geocoders import Nominatim 
from timezonefinder import TimezoneFinder 

# Set up the bot with your API token
bot = telebot.TeleBot("6997327762:AAG0TTlHe0Rx2A5w9OsKJRYYvIGqtBXDLqA")

# Function to get the current time in a given city
def get_world_time(city_name):
    fmt = '%A %Y-%m-%d %H:%M'

    utc = pytz.utc
    utc_now = utc.localize(datetime.datetime.utcnow())
    geolocator = Nominatim(user_agent="MyApp")
    location = geolocator.geocode(city_name)
    
    if location is None:
        return "City not found. Please enter a valid city name."
    
    obj = TimezoneFinder() 
    tz_name = obj.timezone_at(lng=location.longitude, lat=location.latitude) 
    
    if tz_name is None:
        return "Timezone not found for the given city."

    try:
        tz = pytz.timezone(tz_name)
        tz_now = utc_now.astimezone(tz)
        return f'{city_name}: {tz_now.strftime(fmt)}'
    except pytz.exceptions.UnknownTimeZoneError:
        return "Invalid timezone. Please enter a valid timezone."

# Command handler for /tell_world_time
@bot.message_handler(commands=['tell_world_time'])
def tell_world_time(message):
    bot.reply_to(message, "Please enter the city name:")
    bot.register_next_step_handler(message, process_city_name_step)

# Handler for city name input
def process_city_name_step(message):
    try:
        city_name = message.text.strip()
        time_info = get_world_time(city_name)
        bot.reply_to(message, time_info)
    except Exception as e:
        bot.reply_to(message, f"An error occurred: {str(e)}")

# Command handler for /close_world_time
@bot.message_handler(commands=['close_world_time'])
def close_world_time(message):
    bot.reply_to(message, "World time feature disabled. Bot will now echo your messages.")

# Echo handler for normal messages
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

# Start the bot
bot.polling()
