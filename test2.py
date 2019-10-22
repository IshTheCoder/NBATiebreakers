from season import Season

s = Season("division.csv", "games.csv");
s.play_season()
s.league.standings(["Golden State Warriors", 'Los Angeles Lakers'], display=True)

##s.league.standings(s.league.get_conference('West') + s.league.get_conference('East'), display=True)

#s.league.standings(s.league.get_division(s.league.teams['Houston Rockets'].division),display=True)
#print(s.league.get_division('Southwest'))
#print(s.league.is_division_leader('San Antonio Spurs'))
##s.league.global_standings()
##print(s.league.standings(s.league.get_conference('West') + s.league.get_conference('East'), display=True, option='West'))
##print(s.league.split_ties(s.league.standings(s.league.get_conference('West') + s.league.get_conference('East'), display=True, option='West')))
print(s.league.h2h_sort([('Golden State Warriors', 0.8170731708317073), ('San Antonio Spurs', 0.8170731707317073), ('Houston Rockets',0.8170731707317073), ('LA Clippers', 0.8170731707317073), ('Utah Jazz', 0.6219512195121951), ('Oklahoma City Thunder', 0.573170731707317), ('Memphis Grizzlies', 0.524390243902439), ('Portland Trail Blazers', 0.5), ('Denver Nuggets', 0.4878048780487805), ('New Orleans Pelicans', 0.4146341463414634), ('Dallas Mavericks', 0.4024390243902439), ('Sacramento Kings', 0.3902439024390244), ('Minnesota Timberwolves', 0.3780487804878049), ('Los Angeles Lakers', 0.3170731707317073), ('Phoenix Suns', 0.2926829268292683)],option='West'))
print (s.league.h2h_sort([('Boston Celtics', 0.6463414634146342), ('Cleveland Cavaliers', 0.6463414634146342), ('Toronto Raptors',0.6463414634146342), ('Washington Wizards', 0.5975609756097561), ('Atlanta Hawks', 0.524390243902439), ('Milwaukee Bucks', 0.5121951219512195), ('Indiana Pacers', 0.5121951219512195), ('Chicago Bulls', 0.5), ('Miami Heat', 0.5), ('Detroit Pistons', 0.45121951219512196), ('Charlotte Hornets', 0.43902439024390244), ('New York Knicks', 0.3780487804878049), ('Orlando Magic', 0.35365853658536583), ('Philadelphia 76ers', 0.34146341463414637), ('Brooklyn Nets', 0.24390243902439024)]
,option='East'))
print('Ass')
print(s.league.conf_sort([('Boston Celtics', 0.6463414634146342), ('Cleveland Cavaliers', 0.6463414634146342), ('Toronto Raptors',0.6463414634146342),('Washington Wizards',0.6),('Atlanta Hawks', 0.524390243902439)],'East'))
##A={}
##A[3]=['Houston']
##print(A)
