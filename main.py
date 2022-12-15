# Constants
# Goal difference edge cases
GD_EDGE_CASES = {0: 1.0, 1: 1.0, 2: 1.5}
# Starting elo of each team unless specified
STARTING_ELO = 500
# Title of competition
TITLE = "SOCIAL 7-A-SIDE OUTDOOR SOCCER (Mens)"
# Space filler when printing elos to screen
FILLER = 4
# Amount of spaces to the right of the teams when printing
TEAM_RIGHT_SPACE = 2


class Team(object):
    """ Basic team object storing the name and the elo.
    """

    def __init__(self, name: str, elo=STARTING_ELO) -> None:
        self._name = name
        self._elo = elo

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


def goal_index(home_goals: int, away_goals: int) -> float:
    """ Returns the goal index which will help in getting the elo gains of the
    two teams.

    Args:
        home_goals (int): Amount of goals the home team scored
        away_goals (int): Amount of goals the away team scored

    Returns:
        float: The goal index of the match
    """
    goal_difference = abs(home_goals - away_goals)

    # If less than two use edge case mapping as described in wiki
    if goal_difference <= 2:
        return GD_EDGE_CASES[goal_difference]

    return (11 + goal_difference) / 8.0


def get_longest_name() -> str:
    return max(teams, key=lambda team: len(team.get_name())).get_name()


def print_elos() -> None:
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
              " " * left_space + "| ", end="")

        # Prints the elo
        print(space_till_title // 3 * " " + str(team.get_elo()))


# The teams in the competition
teams = [Team("hello"), Team("asasasas")]
# The weight index impacting how important a game is (relating to elo gains)
weight_index = 1.0

if __name__ == "__main__":
    print_elos()
