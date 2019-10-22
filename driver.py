from copy import deepcopy
from season import Season

def sim_season(season, games):
    season_copy = deepcopy(season);
    season_copy.play_season(games);
    return season_copy;

def check_for_elim(season, conf_name, date):
    """
    Checks if a team has been eliminated for the playoffs for a given conference

    TODO what if the last two teams tie, like the situation with the heat and the bulls
    """
    west_copy=[]
    east_copy=[]

    teams = season.league.teams;
    west, east = season.league.standings(season.league.teams,display=False);
    if (conf_name) == "East":
        conf = east;
    else:
        conf = west;

    #TODO what if there are mutliple teams that have this record
    border_team = conf[7][0];
    
    team_to_check = -1;
 
    elimed = [];

    for i in range(len(conf)-1,8,-1):
        if not teams[conf[i][0]].eliminated:
            team_to_check = conf[i][0];
##            print west, east
            break;
    
    if (team_to_check) == -1:
        return [];

    if (teams[team_to_check].total_wins + (82 - teams[team_to_check].games_played) < teams[border_team].total_wins):
        print("{0}: {1} have been eliminated ".format(date, team_to_check));
        elimed.append(team_to_check);
        teams[team_to_check].eliminated = True;
        teams[team_to_check].date_elim = date;
    elif (teams[team_to_check].total_wins + (82 - teams[team_to_check].games_played) == teams[border_team].total_wins):
        #TODO implement ties
        games_left = season.games[season.current_game:];
        for game in games_left:
            if game.home_team == team_to_check:
                game.home_score = game.away_score + 1;
            elif game.away_team == team_to_check:
                game.away_score = game.home_score + 1;
            elif game.home_team == border_team:
                game.home_score = game.away_score - 1;
            elif game.away_team == border_team:
                game.away_score = game.home_score - 1;
        s2 = sim_season(season, games_left);
##        print (s2.league.standings(s2.league.teams))
        west_copy, east_copy = season.league.standings(s2.league.teams,display=False);
        if (conf_name) == "East":
            conf_copy = east_copy;
        else:
            conf_copy = west_copy;
        new_standings = s2.league.h2h_sort(conf_copy, conf_name);
        for j in new_standings[8:]: # if they are in the first 8 now
            if j[0] == team_to_check:
                elimed.append(team_to_check);
                teams[team_to_check].eliminated = True;
                teams[team_to_check].date_elim = date;
                print("{0}: {1} have been eliminated ".format(date, team_to_check));
                break;
                    
    # Need something like this. See lemma
    if (len(elimed) > 0):
        elimed.extend(check_for_elim(s, conf_name, date));
#        print("{0}: {1} have been eliminated ".format(date, elimed[0]));
##        print west, east
##        print west_copy, east_copy
#        print 'West'
#        for i in range(len(west)):
#            print("{0} \t {1:20} \t {2:3f}".format(i+1, west[i][0], west[i][1]));
#        print('East')
#        for i in range(len(east)):
#            print("{0} \t {1:20} \t {2:3f}".format(i+1, east[i][0], east[i][1]));
#        if len(west_copy)>1:
#            west_copy_1, east_copy_1=s2.league.standings(s2.league.teams,display=False);
#              
#            print(' ')
#            print('New copy')
#            for i in range(len(west)):
#                print("{0} \t {1:20} \t {2:3f}".format(i+1, west_copy_1[i][0], west_copy_1[i][1]));
#            print('East copy')
#            for i in range(len(east)):
#                print("{0} \t {1:20} \t {2:3f}".format(i+1, east_copy_1[i][0], east_copy_1[i][1]));



##    print(elimed)

    return elimed


s = Season("division.csv", "games.csv");
for game in s.games:
    s.play_game(game);
    check_for_elim(s, "East", game.date);
    check_for_elim(s, "West", game.date);
with open('stephen_curry.csv','w') as f:
    f.write("Teams, Date Eliminated\n")
    for team in sorted(s.league.teams.keys()):
        if s.league.teams[team].eliminated:
            f.write(s.league.teams[team].name + ',' + s.league.teams[team].date_elim + '\n')
        else: 
            f.write(s.league.teams[team].name + ', Playoffs\n')
