from game import Game
from collections import defaultdict

class Team:
    def __init__(self, name, division, conference):
        self.name = name;
        self.games = defaultdict(list);
        self.division = division;
        self.conference = conference;
        self.total_wins = 0;
        self.games_played = 0;
        self.eliminated = False;
        self.date_elim = "";

    def add_game(self, game, was_home):
        self.games_played += 1;
        if was_home:
            self.games[game.away_team].append(game.home_score - game.away_score);
            if game.home_score > game.away_score:
                self.total_wins += 1;
        else:
            self.games[game.home_team].append(game.away_score - game.home_score);
            if game.away_score > game.home_score:
                self.total_wins += 1;
