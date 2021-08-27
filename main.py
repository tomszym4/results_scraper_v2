import mysql.connector
import datetime
import os
import configparser
import scraper_object as so
import result_checker as rc
import scraper_database as sd

from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


DRIVER_PATH = r"C:\Users\Criminalman\PycharmProjects\webscraper\chromedriver.exe"

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)


"""Checking if config.ini exist"""
if not os.path.isfile('config.ini'):
    print("Config file not found")
    exit(1)
config = configparser.ConfigParser()
config.read('config.ini')

host = config['old_database']['host']
user = config['old_database']['user']
password = config['old_database']['password']
database = config['old_database']['database']


def check_results():
    my_db = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database)
    cursor = my_db.cursor()

    now_date = datetime.datetime.now()
    list_to_check = []

    sql = "SELECT * FROM upcoming_matches"
    cursor.execute(sql)
    temp_upcoming_matches = cursor.fetchall()
    #  Flattening list of tuples from DB

    for item in temp_upcoming_matches:
        n = 0
        upcoming_match = so.PairOfTeams()
        upcoming_match.upcoming_id = item[n]
        upcoming_match.pair_id = item[n+1]
        upcoming_match.date_of_match = item[n+2]
        upcoming_match.postponed = item[n+3]
        upcoming_match.url = item[n+4]
        upcoming_match.url_active = item[n+5]
        upcoming_match.effectivity = item[n+6]
        if upcoming_match.date_of_match + datetime.timedelta(minutes=45, hours=2) <= now_date:
            list_to_check.append(upcoming_match)

    #  Actual checking
    for pair in list_to_check:
        if len(list_to_check) > 0:
            driver.get(pair.url)
            sleep(0.5)
        else:
            print("No upcoming matches to check, exiting")
            closing_chrome()

        #  Checking if postponed/cancelled
        pair.match_postponed = rc.check_if_postponed(driver)
        if not pair.match_postponed:
            pair.result = rc.get_result(driver)

            #  Just double checking
            if pair.result == "-:-":
                pair.match_postponed = 1

            #  Getting results
            pair.result_ht = rc.get_result_ht(driver)
            pair.result_ft = rc.get_result_ft(driver)
            match_goals = rc.get_minutes_of_goals(driver)

            #  TODO making string out of list should get another method
            last_element = len(match_goals) - 1
            for element in match_goals:
                last_element -= 1
                if last_element >= 0:
                    pair.goals += element
                    pair.goals += ","
                else:
                    pair.goals += element

            pair.url_active = 1
        else:
            sd.deleting_entry(my_db, pair.upcoming_id)
            continue

        sd.writing_in_results(my_db, pair)
        sleep(0.1)
    print("DONE checking results")
    closing_chrome()


def closing_chrome():
    driver.close()
    driver.quit()


check_results()
