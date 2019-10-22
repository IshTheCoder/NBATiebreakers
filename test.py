from copy import deepcopy
from season import Season

s = Season("division.csv", "games.csv");
s2 = deepcopy(s);
s.play_season()

print(s.league.teams['Cleveland Cavaliers'].total_wins)
print(s2.league.teams['Cleveland Cavaliers'].total_wins)
#s.play_season()
#s.league.standings(["Golden State Warriors", 'Los Angeles Lakers'], display=True)

#a_var=s.league.standings(s.league.get_conference('West') + s.league.get_conference('East'), display=True)
#print(a_var[7])
#b_var=s.league.standings(s.league.get_conference('West')+s.league.get_conference('East'), conf_merge=False, display=True)
#curr_ties=s.league.global_standings()

