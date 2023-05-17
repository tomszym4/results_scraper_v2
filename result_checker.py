from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


def check_if_postponed(wd):
    """Checks if match was not canceled or postponed"""
    try:
        result = wd.find_element(By.ID, "js-eventstage").text
        if result == "Postponed" or result == "Cancelled" or result == "Abandoned" or result == "After Extra Time":
            return 1
        elif result == "After Penalties":
            score = wd.find_element(By.ID, "js-score").text
            return score
        elif result == "Penalties":
            return result
    except NoSuchElementException:
        result = wd.find_element(By.ID, "js-score").text
        if result == "-:-":
            return 1
        return 0


def get_result(wd):
    """Finds and returns result of a match if WebDriver element provided
    Returns result in string format"""
    try:
        result = wd.find_element(By.ID, "js-score").text
        return result
    except:
        return "N/A Result"


def get_result_ht_ft(wd, after_penalties=False):
    """Finds and returns result for first and second half if WebDriver element is provided
    Returns list of strings"""
    try:
        if after_penalties:
            return clean_goals(wd.find_element(By.ID, "js-partial").text).split(",")[:2]
        return clean_goals(wd.find_element(By.ID, "js-partial").text).split(",")
    except:
        return ["N/A HT Result", "N/A FT Result"]


def get_minutes_of_goals(wd):
    """Returns minutes of scored goals, and check_if_late_goal() should be
    called after this function with goals[] as a parameter"""
    goals = []
    try:
        temp_goals = wd.find_elements(By.TAG_NAME, "td")
        for element in temp_goals:
            temp2 = element.get_attribute("style")
            if temp2 == "width: 4ex; text-align: right;":
                """Getting list of goals without any additional signs (e.g. only 45+2)"""
                temp3 = clean_minutes_of_goals(element.text)
                if temp3.isnumeric():
                    goals.append(temp3)
                elif temp3.find("+") > 0:
                    goals.append(temp3)
        return goals
    except:
        return "N/A minutes of goals"


def clean_minutes_of_goals(temp_string):
    """Returns minutes of match with a '+' if it was in additional time"""
    minute = ""
    for c in temp_string:
        if c.isnumeric():
            minute += c
        elif c == "+":
            minute += c
    return minute


def clean_goals(result):
    goals = ""
    for c in result:
        if c.isnumeric():
            goals += c
        elif c == ":" or c == ",":
            goals += c
    return goals
