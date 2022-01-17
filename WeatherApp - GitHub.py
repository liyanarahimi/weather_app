# Program: Weather App
# Author: Liyana Rahimi
# Description: Program animates real time weather based on user location input

# Imports

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame
import requests

# Data Classes

class images:
    # Stores images used in the app

    # Retrieves local path
    path = os.path.dirname(os.path.realpath(__file__))

    # Blank
    blank = pygame.image.load(path + r"\WeatherAppImages\blank.png")

    # Backgrounds
    sunrise = pygame.image.load(path + r"\WeatherAppImages\sunrise.jpg")
    day = pygame.image.load(path + r"\WeatherAppImages\day.jpg")
    sunset = pygame.image.load(path + r"\WeatherAppImages\sunrise.jpg")
    night = pygame.image.load(path + r"\WeatherAppImages\night.jpg")
    welcome = day

    # Weather Elements
    clouds = pygame.image.load(path + r"\WeatherAppImages\clouds.png")
    rainclouds = pygame.image.load(path + r"\WeatherAppImages\rainclouds.png")
    drizzle = pygame.image.load(path + r"\WeatherAppImages\drizzle.png")
    rain = pygame.image.load(path + r"\WeatherAppImages\rain.png")
    snow = pygame.image.load(path + r"\WeatherAppImages\snow.png")
    lightning = pygame.image.load(path + r"\WeatherAppImages\lightning.png")

# Functional Classes

class weatherData:
    # Obtains live weather info based on user location input

    # API information
    api_url = "https://api.openweathermap.org/data/2.5/weather?"
    api_key = "{insert api key}"

    def __init__(self, location):
        # Sets api url for selected location
        self.url = self.api_url + "q=" + location + "&appid=" + self.api_key
    
    def get(self):
        # Requests current weather data
        response = requests.get(self.url)

        # Checks request status and retrieves data if request was successful
        if response.status_code == 200:
            self.error = False

            # Retrieves data in json format
            data = response.json()

            # Retrieves current time
            self.time = data['dt']

            # Retrieves sunrise
            self.sunrise = data['sys']['sunrise']

            # Retrieves sunset
            self.sunset = data['sys']['sunset']

            # Retrieves wind speed
            self.windspeed = data['wind']['speed']

            # Retrieves weather
            self.weather = data['weather'][0]['main']

        # Reports error
        else:
            self.error = True
            input("There was an error in retrieving weather data from the API. Please input a valid city and try again.") 

class weatherBackground:
    # Determines the background for the weather app based on the time
    
    def __init__(self, now, sunrise, sunset):
        # Prevents sunrise/sunset events ending after 1 second
        sunrise = int(str(sunrise)[:-2])
        sunset = int(str(sunset)[:-2])
        now = int(str(now)[:-2])

        # Checks current daylight status and sets background
        # Checks for is sunrise
        if now == sunrise:
            self.screen = images.sunrise
        # Checks for is daytime
        elif now > sunrise and now < sunset:
            self.screen = images.day
        # Checks for is sunset
        elif now == sunset:
            self.screen = images.sunset
        # Accounts for nightime
        else:
            self.screen = images.night

class weatherElements:
    # Determines live weather elements for the weather app

    # Resets elements
    x = images.blank
    y = images.blank
    z = images.blank

    def __init__(self, element):
        # Checks for drizzle
        if element == "Drizzle":
            self.x = images.rainclouds
            self.y = images.drizzle
        # Checks for rain
        elif element == "Rain":
            self.x = images.rainclouds
            self.y = images.rain
        # Checks for thunderstorms
        elif element == "Thunderstorm":
            self.x = images.rainclouds
            self.y = images.rain
            self.z = images.lightning
        # Checks for clouds
        elif element == "Clouds":
            self.x = images.clouds
        # Checks for snow
        elif element.lower() == "Snow":
            self.y = images.snow

# Main Program - Weather App

class weatherApp:
    def __init__(self):
        # Displays welcome message
        input("Welcome. This is an animated weather simulator. ")

        # Loops API request until data retrieval is successful
        while True:
            # Prompts user to select a location
            city = input("Please select a city: ")

            # Title-cases location for API request
            city = city.title()

            # Sends API request for weather data
            data = weatherData(city)
            data.get()

            # Retrieves error status
            if data.error == False: 
                break

        # Initializes pygame 
        pygame.init()

        # Sets app clock
        clock = pygame.time.Clock()

        # Sets screen size
        self.display = (800,600)
        self.screen = pygame.display.set_mode(self.display)

        # Counter for background loop
        b = 0

        # Counters for element loops
        x = 0
        y = 0
        z = 0
        
        # App loop
        running = True
        while running:
            # Sets app fps
            clock.tick(5)

            # Gets live weather data
            data.get()

            # Sets app background and elements
            background = weatherBackground(data.time, data.sunrise, data.sunset)
            elements = weatherElements(data.weather)

            # Diplays background
            self.screen.blit(background.screen, (b, 0))
            self.screen.blit(background.screen, (self.display[0] + b, 0))

            # Displays horizontal elements
            self.screen.blit(elements.x, (x, 0))
            self.screen.blit(elements.x, (x - self.display[0], 0))

            # Displays vertical elements
            self.screen.blit(elements.y, (0, y))
            self.screen.blit(elements.y, (0, y - self.display[1]))
        
            # Loops background
            if (b<=-self.display[0]):
                b = 0
            b-=1

            # Loops horizontal elements based on current windspeed
            if (x>=self.display[0]):
                x = 0
            x+=data.windspeed

            # Loops vertical elements
            if (y>=self.display[1]):
                y = 0
            y+=5

            # Displays periodic elements intermittently
            if (z==10):
                self.screen.blit(elements.z, (0, 0))
                z = 0
            z+=1

            # Updates display screen
            pygame.display.update()

            # Quits app
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()

# Running Program

weatherApp()