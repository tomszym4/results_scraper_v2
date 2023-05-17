import mysql.connector
import datetime
import os
import configparser
import scraper_object as so
import result_checker as rc
import scraper_database as sd
import re

from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


driver_path = r"/Users/tszymanski/PycharmProjects/web_scraper_v3/chromedriver"

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(options=options, executable_path=driver_path)


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


def check_if_late(goals_minutes):
    """Takes list with minutes of goals and checks if goals in game was late (after 35' or 75')
    and should be called after get_minutes_of_goals returns bool value"""
    was_late = False
    was_ht_late = False
    was_ft_late = False
    for list_element in goals_minutes:
        try:
            if 30 <= int(list_element) <= 45:
                was_late = True
                was_ht_late = True
            elif 75 <= int(list_element) <= 90:
                was_late = True
                was_ft_late = True
        except ValueError:
            if re.search("45+", list_element):
                was_late = True
                was_ht_late = True
            elif re.search("90+", list_element):
                was_late = True
                was_ft_late = True
    return was_late, was_ht_late, was_ft_late


def check_results():
    my_db = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database)
    cursor = my_db.cursor()

    now_date = datetime.datetime.now()
    today_date = now_date - datetime.timedelta(hours=2, minutes=45)
    sql = "SELECT * FROM upcoming_matches WHERE date_of_match < %s"
    cursor.execute(sql, (today_date,))
    upcoming_matches = cursor.fetchall()
    pairs = []
    for item in upcoming_matches:
        n = 0
        upcoming_match = so.PairOfTeams()
        upcoming_match.upcoming_id = item[n]
        upcoming_match.pair_id = item[n+1]
        upcoming_match.date_of_match = item[n+2]
        upcoming_match.postponed = item[n+3]
        upcoming_match.url = item[n+4]
        upcoming_match.url_active = item[n+5]
        upcoming_match.effectivity = item[n+6]
        pairs.append(upcoming_match)

    if not pairs:
        print("No upcoming matches to check, exiting")
        closing_chrome()

    for pair in pairs:
        driver.get(pair.url)
        print(pair.url)
        sleep(0.5)
        pair.match_postponed = rc.check_if_postponed(driver)
        if pair.match_postponed == "Penalties":
            continue
        if not pair.match_postponed or pair.match_postponed == "After Penalties":
            pair.result = rc.get_result(driver)

            if pair.match_postponed == "After Penalties":
                pair.result_ht, pair.result_ft = rc.get_result_ht_ft(driver, after_penalties=True)
            else:
                pair.result_ht, pair.result_ft = rc.get_result_ht_ft(driver)
            pair.goals = ','.join(rc.get_minutes_of_goals(driver))
            pair.is_late, pair.is_ht_late, pair.is_ft_late = check_if_late(pair.goals.split(","))
            pair.url_active = 1
        else:
            sd.deleting_entry(my_db, pair.upcoming_id)
            print(f"deleting this one - {pair.url}")
            continue
        # TODO: checking effectivity and then deleting a pair with results if last match would be under 8/10 eff.
        sd.writing_in_results(my_db, pair)
        sleep(0.1)

    print("DONE checking results")
    closing_chrome()


def closing_chrome():
    driver.close()
    driver.quit()


check_results()
