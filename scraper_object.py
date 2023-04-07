import datetime


class UpcomingMatches:
    def __init__(self):
        self.id = 0
        self.pair_id = 0
        self.date_of_match = datetime.datetime.now()
        self.postponed = 0
        self.url = ""
        self.url_active = 1


class PairOfTeams:
    def __init__(self):
        self.pair_id = 0
        self.team_1_name = ""
        self.team_1_id = 0
        self.team_2_name = ""
        self.team_2_id = 0
        self.country = ""
        self.league = ""
        self.effectivity = 0
        self.ht_effectivity = 0
        self.ft_effectivity = 0
        self.total_matches = 0
        self.last_updated = datetime.datetime.now()
        #  ---------------------------------
        self.postponed = 0
        self.url = ""
        self.url_active = 1
        self.goals = []
        self.upcoming_id = 0
        self.ht_result = ""
        self.ft_result = ""
        self.date_of_match = datetime.datetime.now()


class Results:
    def __init__(self):
        self.id = 0
        self.pair_id = 0
        self.result = ""
        self.first_half = ""
        self.second_half = ""
        self.goals = []
        self.date_of_match = datetime.datetime.now()
        self.postponed = 0
        self.url = ""
        self.url_active = 1
        self.is_ht_late = 0
        self.is_ft_late = 0
        self.is_late = 0


"""def print_all_info(scraper_object):
    stats = "----------------------------------------------------------------\n" \
            "{} - {} at {}\n" \
            "ID {} - {} vs. ID {} - {}\n" \
            "Effectiveness: {}\n" \
            "Link: {}"
    print(stats.format(scraper_object.country, scraper_object.league, scraper_object.date_of_match,
                       scraper_object.home_team_id, scraper_object.home_team,
                       scraper_object.away_team_id, scraper_object.away_team,
                       scraper_object.effectiveness, scraper_object.link))
"""
