from bs4 import BeautifulSoup # Library to parse the saits
import requests # Library to make requests to the saits
import pymysql

import logging
from aiogram import Bot, Dispatcher, types, executor

from graphic import build_graph
from config import host, user, password, db_name, token

# Сайт для парсинга
# https://world-weather.ru/


logging.basicConfig(level=logging.INFO)
bot = Bot(token=token)
dp = Dispatcher(bot)

# Greeting function
@dp.message_handler(commands=["start"])
async def hello_message(message: types.Message):
    await message.answer("Здравствуйте, введите комманду /forecast и название города для получение прогноза погоды")

@dp.message_handler(commands=["forecast"])
async def forecast(message: types.Message):
    city_name = message.text.split()[1]

    # Creating connection to DB
    try:
        connection = pymysql.connect(
            host=host,
            port=3306,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )

        try:
            with connection.cursor() as cursor:
                # Link to parse the sait
                global URL
                URL = ""
                
                # Selecting link of the city from database
                query = f"SELECT city, link FROM links WHERE city = '{city_name}';"
                cursor.execute(query)
                city_and_link = cursor.fetchall()[0]
                city = city_and_link["city"]
                link = city_and_link["link"]
                print(city)
                print(link)

                URL = f"{link}/24hours"
        except Exception as ex:
            print(ex)

    # Printing the error if it is
    except Exception as ex:
        print("Connection refused...")
        print(ex)



    # Staff to make requests to site
    HEADERS = {
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Mobile Safari/537.36",
        "accept": "*/*"
    }

    # Making request to site
    response = requests.get(url=URL, headers=HEADERS)

    # If site's request is good copy all page in veriable
    if response.status_code == 200:
        # Making the veriable to parse a site
        city_page = BeautifulSoup(response.text, "html.parser")

        # Parsing
        # Looking for times of temperatures
        times_poor = city_page.find_all("div", class_="weather-day")
        times_pure = []
        # Transformating times data from html format to string
        for i in times_poor:
            times_pure.append(str(i).split(">")[1][:-5])
            if "23:00" in i:
                break
        data_lenght = len(times_pure)


        # Looking for temperature recording
        temps_poor = city_page.find_all("div", class_="weather-temperature")[:data_lenght]
        temps_pure = []
        # Transformating temps data from html format to string
        for i in temps_poor:
            temps_pure.append(str(i).split(">")[1][:-5])


        # # Printing the times in list
        # print("Times:", times_pure)

        # # Printing the temperatures in list
        # print("Temps:", temps_pure)

        pure_data = list(zip(times_pure, temps_pure))
        # # Printing data into console
        # for i in pure_data:
        #     print(f"{i[0]}: {i[1]}")
        
        await message.answer(pure_data)

        # Building a graphic
        build_graph(times=times_pure, temps=temps_pure, data_lenght=data_lenght, city=city) # X scale — times, Y scale — temperatures

        # Sending photo of graphic to user
        with open('forecast.png', 'rb') as photo: # Preparing photo before sending
            await message.answer_photo(photo, caption=f"Прогоноз погоды в городе {city_name}") # Sending photo to user


if __name__ == "__main__":
    executor.start_polling(dp,skip_updates=True)