from bs4 import BeautifulSoup # Library to parse the saits
import pymysql.cursors
import requests # Library to make requests to the saits
import pymysql

from config import host, user, password, db_name

# Сайт для парсинга
# https://world-weather.ru/archive/

# Link to parse the sait
URL = "https://world-weather.ru/archive/"


# Stuff for making requests to the site "world-weather.ru"
HEADERS = {
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36",
    "accept": "*/*"
}

archive_response = requests.get(url=URL, headers=HEADERS) # Making request to site

if archive_response.status_code == 200: # Checking the correctness of connecting
    # Copying a whole page
    site = BeautifulSoup(archive_response.text, "html.parser") # The code of site

    # Parsing links of counries from site and converting them in a proper form

    # The first version of code which is unreadable
    # countres_links = [[str(j).split()[1][6:-1] for j in i.find_all("a")] for i in site.find_all("div", "list-plases")]

    # The second version of code which better than earlier
    countries = site.find_all("div", class_="list-plases") # Parsing all tags "a" with nesseccary links
    countries_links = [] # Creating a new list for pure links
    # Scaning all tags from list "countries"
    for i in countries:
        for j in i.find_all("a"): # Searching tags "a" with links in a generalized tags
            countries_links.append(str(j).split()[1][8:-1]) # Separating links from tags and doing links more readable and ready for using
    

    # Deleting odd stuff from list of links
    for id, i in enumerate(countries_links):
            if not ("weather" in i):
                del countries_links[id]

    # Output all countries links in a another file
    # with open("countries_links.txt", "w+", encoding="utf-8") as f:
    #     for i in countries_links:
    #         f.write(i + "\n")

    # Variable "countries_links" is a list and ready for using
    

# Parsing each page of country and taking a links of cities into another file

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
    print("Successfully connected...")
    # Parsing each page of country
    for i in countries_links:
        COUNTRY_URL = "https://" + i # Creating url of the each page of country
        country_response = requests.get(url=COUNTRY_URL, headers=HEADERS) # Making requests to each page of country
        country_page = BeautifulSoup(country_response.text, "html.parser") # The code of site


        if country_response.status_code == 200: # Checking the correctness of connecting
            # Separating cities' tags from country page

            # The first version of code which is unreadable
            # cities = [str(j).split()[1][8:-1] for j in country_page.find("div", class_="list-cities").find_all("a")]

            # The second version of code
            # Separating links from tags and transformating them in proper form
            for tag in country_page.find("div", class_="list-cities").find_all("a"):
                link = str(tag).split()[1][8:-1] # Separating links from tags
                if "weather" in link: # Checking the filling of tag
                    city_name = str(tag).split(">")[1][:-3]
                    link = "https://" + link.split("/")[0] + "/" + "pogoda" + "/" + "/".join(link.split("/")[2:-2]) # Transformating the link

                    query = f'INSERT INTO links (city, link) VALUES ("{city_name}", "{link}");' # Query to DB (add city and link)
                    # Adding city and link into DB
                    try:
                        with connection.cursor() as cursor:
                            cursor.execute(query) # Executing the query
                        connection.commit()
                    except:
                        pass


            print(i + ": Обработанно") # Printing successful result for each country

# Printing the error if it is
except Exception as ex:
    print("Connection refused...")
    print(ex)