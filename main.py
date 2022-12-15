# Imports
import json


# Constants
# Goal difference edge cases
GD_EDGE_CASES = {0: 1.0, 1: 1.0, 2: 1.5}
# Starting elo of each team unless specified
STARTING_ELO = 1000
# Title of competition
TITLE = "SOCIAL 7-A-SIDE OUTDOOR SOCCER (Mens)"
# Space filler when printing elos to screen
FILLER = 4
# Amount of spaces to the right of the teams when printing
TEAM_RIGHT_SPACE = 2
# The magnification factor of the elo gains/losses
MAGNIFICATION = 100.0

# The teams in the competition
teams = []


class Team(object):
    """ Basic team object storing the name and the elo.
    """
    def __init__(self, name: str, elo=STARTING_ELO, points = 0) -> None:
        self._name = name
        self._elo = elo
        self._points = points

    def get_name(self) -> str:
        return self._name

    def get_elo(self) -> float:
        return self._elo

    def update_elo(self, new_elo: float) -> None:
        self._elo = new_elo


def expected_result(elo_home: float, elo_away: float) -> float:
    """ Returns the expected probability of the home team winning.
    Uses a system similar to the one found in the World Football Elo Ratings.

    Args:
        elo_home (int): Elo from the home team
        elo_away (int): Elo from the away team

    Returns:
        float: The expected probability of the home team winning
    """
    return 1 / (pow(10, -abs(elo_home - elo_away) / 400) + 1)


def goal_index(goal_difference: int) -> float:
    """ Returns the goal index which will help in getting the elo gains of the
    two teams.

    Args:
        home_goals (int): Amount of goals the home team scored
        away_goals (int): Amount of goals the away team scored

    Returns:
        float: The goal index of the match
    """
    # If less than two use edge case mapping as described in wiki
    goal_difference = abs(goal_difference)
    if goal_difference <= 2:
        return GD_EDGE_CASES[goal_difference]

    return (11 + goal_difference) / 8.0


def get_longest_name() -> str:
    return max(teams, key=lambda team: len(team.get_name())).get_name()


def print_elos() -> None:
    """ Prints the elos of the teams in the terminal. The elos printed are sorted
    from largest elo to the smallest elo.
    """
    # Prints title
    print(" " * FILLER + TITLE + " " * FILLER)
    print((len(TITLE) + 2 * FILLER) * "-")

    # Sort teams of descending order based on elo
    teams.sort(key=lambda team: team.get_elo(), reverse=True)
    length = len(get_longest_name()) + TEAM_RIGHT_SPACE
    space_till_title = (len(TITLE) + 2 * FILLER) - length

    for counter, team in enumerate(teams):
        # Prints Names of each team
        left_space = length - len(team.get_name())
        print(f"{counter + 1}. {team.get_name()}" +
              " " * (left_space - ((counter + 1) // 10)) + "| ", end="")

        # Prints the elo
        print(space_till_title // 3 * " " + str(round(team.get_elo(), 2)))


def update_points(name_home: str, name_away: str, gd: int) -> None:
    """ Updates the elo of the team based on goal difference

    Args:
        name_home (str): Name of the home team
        name_away (str): Name of the away team
        gd (int): The goal difference in perspective of the home team
    """
    if name_home not in [team.get_name() for team in teams]:
        teams.append(Team(name_home))

    if name_away not in [team.get_name() for team in teams]:
        teams.append(Team(name_away))

    # Calculate amount elo gained/lossed
    for team in teams:
        if team.get_name() == name_home:
            team_home = team
        elif team.get_name() == name_away:
            team_away = team

    # Result is 0.5 if draw, 1 if win 0 if lose
    home_result = 0.5 if gd == 0 else int(gd > 0)
    away_result = 0.5 if gd == 0 else int(gd < 0)

    # Updates elos
    team_home.update_elo(team_home.get_elo() + point_calculation(goal_index(gd),
                         home_result, expected_result(team_home.get_elo(), team_away.get_elo())))
    team_away.update_elo(team_away.get_elo() + point_calculation(goal_index(gd),
                         away_result, 1 - expected_result(team_away.get_elo(), team_home.get_elo())))


def point_calculation(goal_index: float, result: float, expected: float) -> None:
    """ Does the final calculation of how much each time should win or lose.

    Args:
        goal_index (float): The magnitute factor from the goal difference
        result (float): 1 if home team, 0.5 if draw 0 if away team won
        expected (float): based on elo who was meant to win
    """
    return MAGNIFICATION * goal_index * (result - expected)


def read_data() -> None:
    """ Reads the data from json file provided by the scraper then updates the elo.
    """
    with open('game_data.json') as json_file:
        data = json.load(json_file)

    for match in data.values():
        home_name, away_name = match["team_1"]["name"], match["team_2"]["name"]
        gd = match["team_1"]["goals"] - match["team_2"]["goals"]
        update_points(home_name, away_name, gd)


if __name__ == "__main__":
    read_data()
    print_elos()

