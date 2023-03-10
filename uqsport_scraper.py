from bs4 import BeautifulSoup
import requests
import json

"""
Results={
    match_i:{
        team_1:{
            name: str,
            goals: int,
        },
        team_2:{
            name: str,
            goals: int,
        },
        division: int
    }
}
"""

RESULTS = {}
DATES = ["2022-12-04", "2022-12-11", "2022-12-18", "2023-01-22", "2023-01-29"]

match_id = 0

# Iterates through all possible dates
for date in DATES:
    url = f"https://teams.uqsport.com.au/Team/Round/1464/2/{date}"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    matches = soup.find_all("div", class_="fxt")

    # Iterates through all the matches except the last which is always a bye
    for match in matches[0:-1]:
        # Gets the div team div element and then it's childs text which is the team name
        team_1 = match.find("div", class_="fxt__item--team-home")
        team_2 = match.find("div", class_="fxt__item--team-away")
        team_1_name = team_1.find("a").text
        team_2_name = team_2.find("a").text

        # Team goals
        print(f"team 1 {team_1_name}, team 2 {team_2_name}, date {date}")
        team_1_goals = int(match.find(
            "div", class_="fxt__item--score-home").contents[0])
        team_2_goals = int(match.find(
            "div", class_="fxt__item--score-away").contents[0])

        # Calculates who won the match
        winner = 0 if team_1_goals == team_2_goals else int(
            team_1_goals < team_2_goals) + 1

        # Stores the data in the dictionary and increment match_id
        RESULTS[f"match_{match_id}"] = {
            "team_1": {
                "name": team_1_name,
                "goals": team_1_goals,
            },
            "team_2": {
                "name": team_2_name,
                "goals": team_2_goals,
            }
        }
        match_id += 1

# Converts the dictionary into json and saves it
RESULTS = json.dumps(RESULTS, indent=4)
with open('game_data.json', 'w') as outfile:
    outfile.write(RESULTS)
