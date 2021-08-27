
def check_if_postponed(wd):
    """Checks if match was not canceled or postponed"""
    try:
        result = wd.find_element_by_id("js-eventstage").text
        if result == "Postponed":
            print("Postponed")
            return 1
        elif result == "Canceled":
            print("Canceled")
            return 1
        elif result == "Penalties":
            #  TODO: Look if return 1 of other number and not delete upcoming_match
            return 1
        else:
            return 0
    except:
        return 0


def get_result(wd):
    """Finds and returns result of a match if WebDriver element provided
    Returns result in string format"""
    try:
        result = wd.find_element_by_id("js-score").text
        return result
    except:
        return "N/A Result"


def get_result_ht(wd):
    """Finds and returns result of a first half if WebDriver element provided
    Returns result in string format"""
    try:
        result = wd.find_element_by_id("js-partial").text
        ht = clean_goals(result)
        ht = ht.split(",")
        return ht[0]
    except:
        return "N/A HT Result"


def get_result_ft(wd):
    """Finds and returns result of a second half if WebDriver element provided
    Returns result in string format"""
    try:
        result = wd.find_element_by_id("js-partial").text
        ft = clean_goals(result)
        ft = ft.split(",")
        return ft[1]
    except:
        return "N/A FT Result"


def get_minutes_of_goals(wd):
    """Returns minutes of scored goals,
    and check_if_late_goal() should be
    called after this function with goals[]
    as a parameter"""
    goals = []
    try:
        temp_goals = wd.find_elements_by_tag_name("td")
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
    list_goals = []
    goals = ""
    for c in result:
        if c.isnumeric():
            goals += c
        elif c == ":" or c == ",":
            goals += c
    return goals
