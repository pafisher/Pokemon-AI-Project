import log

DESOLATELAND = "DESOLATELAND"
HAIL = "HAIL"
PRIMORDIALSEA = "PRIMORDIALSEA"
RAINDANCE = "RAINDANCE"
SANDSTORM = "SANDSTORM"
SUNNYDAY = "SUNNYDAY"

weather = ""
weather_countdown = 0

def get_weather():
	return weather

def set_weather(new_weather, new_countdown):
	global weather
	global weather_countdown
	weather = new_weather
	weather_countdown = new_countdown
	if (new_weather == DESOLATELAND):
		log.message("The sun is shining brightly")
	elif (new_weather == HAIL):
		log.message("It started to hail")
	elif (new_weather == PRIMORDIALSEA):
		log.message("It started to rain")
	elif (new_weather == RAINDANCE):
		log.message("It started to rain")
	elif (new_weather == SANDSTORM):
		log.message("A sandstorm whipped up")
	elif (new_weather == SUNNYDAY):
		log.message("The sun is shining brightly")

def clear_weather():
	global weather
	global weather_countdown
	log.message("The weather cleared up")
	weather = ""
	weather_countdown = 0

def decrement_weather():
	global weather_countdown
	weather_countdown -= 1

def get_weather_countdown():
	return weather_countdown