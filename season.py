from league import League
from game import Game

class Season:
    def __init__(self, league_path, game_path):
        self.league = League(league_path);
        self.games = [];
        self.current_game = 0;
        with open(game_path, 'r') as f:
            for line in f:
                data = line.split(',');
                self.games.append(Game(data[0], data[1], data[2], int(data[3]), int(data[4])));

    def play_game(self, game):
        """
         Plays a game
         """
        self.current_game += 1;
        self.league.teams[game.home_team].add_game(game, True);
        self.league.teams[game.away_team].add_game(game, False);

    def play_season(self, games):
        for game in games:
            self.play_game(game);
