from team import Team

class League:
    def __init__(self, path):
        self.teams = {}
        with open(path,'r') as f:
            for line in f:
                data = line.split(',');
                self.teams[data[0]] = Team(data[0], data[1], data[2]);

    def get_conference(self, key):
        conf = [];
        for team in self.teams.keys():
           if self.teams[team].conference == key:
               conf.append(team);
        return conf;

    def get_division(self, key):
        div = [];
        for team in self.teams.keys():
           if self.teams[team].division == key:
               div.append(team);
        return div;

    def get_division_team(self, team):
        return self.get_division(self.teams[team].division)
        
    def standings(self, teams, conf_merge=False, display=False, option='Both'):
        """
        returns the standings among the given teams
        """
        percents = [];
        percents_east=[]
        percents_west=[]
        for team_a in teams:
            wins = 0;
            games_played = 0
            for team_b in teams:
                if team_a != team_b:
                    wins += len([1 for score_diff in self.teams[team_a].games[team_b] if score_diff > 0]);
                    games_played += len(self.teams[team_a].games[team_b]);

            if games_played == 0:
                games_played = 1;
            if self.teams[team_a].conference=='West':
                percents_west.append((team_a, float(wins)/games_played))
            else:
                percents_east.append((team_a, float(wins)/games_played))
        if conf_merge:
            percents=percents_west+percents_east
            percents = sorted(percents, key=lambda k: k[1], reverse=True);
            if display:
                for i in range(len(percents)):
                    print("{0} \t {1:20} \t {2:3f}".format(i+1, percents[i][0], percents[i][1]));

            return percents
        else:
            percents_west = sorted(percents_west, key=lambda k: k[1], reverse=True);
                    
                
            if display:
                print("West");
                for i in range(len(percents_west)):
                    print("{0} \t {1:20} \t {2:3f}".format(i+1, percents_west[i][0], percents_west[i][1]));

            percents_east = sorted(percents_east, key=lambda k: k[1], reverse=True);


            if display:
                print("East");
                for i in range(len(percents_east)):
                    print("{0} \t {1:20} \t {2:3f}".format(i+1, percents_east[i][0], percents_east[i][1]));
            if option=='West':
                return percents_west
            elif option=='East':
                return percents_east
            
            return percents_west, percents_east


            

    def global_standings(self, display=True):
        percents_west=self.standings(self.teams.keys(),conf_merge=False,option='West')
        percents_east=self.standings(self.teams.keys(),conf_merge=False,option='East')
        percents_east=self.h2h_sort(percents_east,'East')
        percents_west=self.h2h_sort(percents_west,'West')
        final_stand=self.h2h_sort(percents_west,'West')+self.h2h_sort(percents_east,'East')
        if display:
            for i in range(len(percents_west)):
                print("{0} \t {1:20} \t {2:3f}".format(i+1, percents_west[i][0], percents_west[i][1]));

        percents_east = sorted(percents_east, key=lambda k: k[1], reverse=True);


        if display:
            for i in range(len(percents_east)):
                print("{0} \t {1:20} \t {2:3f}".format(i+1, percents_east[i][0], percents_east[i][1]));
        
        return final_stand

    def tie_break_two(self, team_a, team_b):
        """
        Takes in two teams in a tie and returns them in the proper order
        """
        # First check the head to head record
        percents = self.standings([team_a,team_b], conf_merge=True);
        if (percents[0][1] != percents[1][1]):
            return [ele[0] for ele in percents];
        
        # Second check if one team is divison leader
        div_a = self.is_division_leader(team_a, team_a.conference);
        div_b = self.is_division_leader(team_b, team_b.conference);
        if div_a and not div_b:
            return [team_a, team_b];
        elif not div_a and div_b:
            return [team_b, team_a];
         
        # Thrid division W/L if they are same division
        if team_a.division == team_b.division:
            div_list = self.get_division(team_a.division);
            div_stand = self.standings(div_list, conf_merge=True);
            div_a_percent = -1;
            div_b_percent = -1;
            for ele in div_stand:
                if ele[0] == team_a:
                    div_a_percent = ele[1];
                if ele[0] == team_b:
                    div_b_percent = ele[1];
            
            if div_a_percent > div_b_percent:
                return [team_a, team_b];
            elif div_a_percent < div_b_percent:
                return [team_b], [team_a];
        
        # Forth conference W/L
        conf_list = self.get_conference(team_a.conference);
        conf_stand = self.standings(conf_list, conf_merge=True);
        conf_a_percent = -1;
        conf_b_percent = -1;
        for ele in conf_stand:
            if ele[0] == team_a:
                conf_a_percent = ele[1];
            if ele[0] == team_b:
                conf_b_percent = ele[1];
        if conf_a_percent > conf_b_percent:
            return [team_a, team_b];
        elif conf_a_percent < conf_b_percent:
            return [team_b, team_a];
       
        # Fifth standings against non eliminated teams in conference 
        conf_list = [team for team in self.get_conference(team_a.conference) if not team.eliminated];
        conf_stand = self.standings(conf_list, conf_merge=True);
        conf_a_percent = -1;
        conf_b_percent = -1;
        for ele in conf_stand:
            if ele[0] == team_a:
                conf_a_percent = ele[1];
            if ele[0] == team_b:
                conf_b_percent = ele[1];
        if conf_a_percent > conf_b_percent:
            return [team_a, team_b];
        elif conf_a_percent < conf_b_percent:
            return [team_b, team_a];
 
        # Sixth standings against non-eliminated teams in other conference
        if team_a.conference == "West":
            other_conf = "East";
        else:
            other_conf = "West";

        conf_list = [team for team in self.get_conference(other_conf) if not team.eliminated];
        conf_stand = self.standings(conf_list, conf_merge=True);
        conf_a_percent = -1;
        conf_b_percent = -1;
        for ele in conf_stand:
            if ele[0] == team_a:
                conf_a_percent = ele[1];
            if ele[0] == team_b:
                conf_b_percent = ele[1];
        if conf_a_percent > conf_b_percent:
            return [team_a, team_b];
        elif conf_a_percent < conf_b_percent:
            return [team_b, team_a];

        #Finally we have point differenial
        pd_a = 0;
        for opp in team_a.games.values():
            pd_a += sum(opp);
        pd_b = 0;
        for opp in team_b.games.values():
            pd_b += sum(opp);
        if pd_a > pd_b:
            return [team_a, team_b];
        else:
            return [team_b, team_a];


##    def seed_corrector(self, teams, pre_div=True, display=False):
##        percents_west=self.standings(teams,conf_merge=False,option='West')
##        percents_east=self.standings(teams,conf_merge=False,option='East')
##        western_ties, west_tie_seeds=self.find_ties(percents_west)
##        eastern_ties, east_tie_seeds=self.find_ties(percents_east)
##        
####        print(western_ties[0][0], west_tie_seeds)
####        print(self.standings(['LA Clippers','Utah Jazz']))
##        for j in range(len(western_ties)):
##            team_list=[]
##            for element in western_ties[j]:
##                team_list.append(element[0])
##            print team_list
##            new_order= self.standings(team_list)
##            if pre_div==True:
##                still_ties=self.find_ties(new_order)
##                
####            if len(still_ties[0])>0:
####                print('DAMN.')
####                print(still_ties)
####            else:
####                print('Grimy')
##                
##            tie_teams=[]
##            for ele in new_order:
##                tie_teams.append((ele[0],western_ties[j][0][1]))
##            del percents_west[west_tie_seeds[j][0]:west_tie_seeds[j][-1]]
##            percents_west[west_tie_seeds[j][0]:west_tie_seeds[j][-1]]=new_order
##            
##        for k in range(len(eastern_ties)):
##            team_list=[]
##            for element in eastern_ties[k]:
##                team_list.append(element[0])
####            print(team_list)
##            new_order= self.standings(team_list)
####            print new_order
##            tie_teams=[]
##            for ele in new_order:
##                tie_teams.append((ele[0],eastern_ties[k][0][1]))
##            del percents_east[east_tie_seeds[k][0]:east_tie_seeds[k][-1]]
##            
##                
##            percents_east[east_tie_seeds[k][0]:east_tie_seeds[k][-1]]=tie_teams
##        if display:
##            for i in range(len(percents_west)):
##                print("{0} \t {1:20} \t {2:3f}".format(i+1, percents_west[i][0], percents_west[i][1]));
##
##        percents_east = sorted(percents_east, key=lambda k: k[1], reverse=True);
##
##
##        if display:
##            for i in range(len(percents_east)):
##                print("{0} \t {1:20} \t {2:3f}".format(i+1, percents_east[i][0], percents_east[i][1]));
##        
####        print percents_east
##            
##        return percents_west + percents_east
    
    def h2h_sort(self, percents,option,global_no_ties=False):
        """Takes in a league, a standings i.e. a list of tuples (team, team_record)
        finds the ties, and sorts them into the correct order, in case the global_no_ties
        variable is still False, even after the h2h and division chamption cannot sort any further, then we
        call the conference record sorter"""
        ties,tie_seeds=self.find_ties(percents)
        if len(ties)==0:
            
            global_no_ties=True
            return percents
        

        for j in range(len(ties)):
            if len(ties[j])>2:
                new_order_1,new_order_2= self.div_lead_sort(ties[j],option)
##
##                if new_order_1!=self.h2h_sort(new_order_1,option):
##                    new_order_1=self.h2h_sort(new_order_1,option)

##                if new_order_1==self.h2h_sort(new_order_1,option) and global_no_ties==False:
##                    self.conf_sort(new_order_1,option)
##                if new_order_2!=self.h2h_sort(new_order_2,option):
##                    new_order_2=self.h2h_sort(new_order_2,option)
##                if new_order_2==self.h2h_sort(new_order_2,option) and global_no_ties==False:
##                    print('Blah')
####                    new_order_1=self.conf_sort(new_order_1,option)
##                    new_order_2=self.conf_sort(new_order_2,option)
                new_order=new_order_1+new_order_2
##                print('Stormzy')
##                print(new_order)
            else:
                
                team_list=[]
                for element in ties[j]:
                    team_list.append(element[0])
                
                new_order= self.standings(team_list,option)
##                if new_order!=self.h2h_sort(new_order,option):
##                    new_order=self.h2h_sort(new_order,option)
##                if new_order==self.h2h_sort(new_order,option) or len(self.find_ties(new_order))>0:
##                    new_order=self.conf_sort(new_order,option)
                
    ##            if pre_div=True:
    ##                still_ties=self.find_ties(new_order)
    ##                
    ##            if len(still_ties[0])>0:
    ##                print('DAMN.')
    ##                print(still_ties)
    ##            else:
    ##                print('Grimy')
##            print('Stormz')
##            print(new_order)
            tie_teams=[]
            for ele in new_order:
                tie_teams.append((ele[0],ties[j][0][1]))
##            print(tie_seeds[j][-1])
##            del percents[tie_seeds[j][0]-1:tie_seeds[j][-1]]
##            print(percents)
##            print(tie_teams)
            percents[tie_seeds[j][0]-1:tie_seeds[j][-1]]=tie_teams
##        print(percents)
        return percents

        
        
    def find_ties(self, percents):
        """This function takes in a league, and takes in the percents, i.e. a list of tuples,
        with the teams as the first tuple element and the win % as the second element of the
        tuple. It then spits out a list containing a list of every team that is tied, in tuple
        form with the first element as the team and the second element as a tuple."""
        ties_list=[]
        curr_tie=[]
        tie_seedings=[]
        curr_tie_seed=[]
        tie=True
        for index in range(len(percents)-1):
            if tie==False:
                if len(curr_tie)>0:
                    
                    ties_list.append(curr_tie)
                    tie_seedings.append(curr_tie_seed)
                    curr_tie=[]
                    curr_tie_seed=[]

                
                
                
            if percents[index][1]==percents[index+1][1]:
                tie=True
            else:
                tie=False
            if tie==True:
                curr_tie.append(percents[index])
                curr_tie.append(percents[index+1])
                curr_tie_seed.append(index)
                curr_tie_seed.append(index+1)

        ties_list,tie_seedings=self.split_ties(percents) 
        return ties_list, tie_seedings

    def is_division_leader(self,team,option):
        """Checks if team is a division leader and returns true or false."""
        
        is_leader=False
        aa=self.standings(self.teams.keys(),option,display=True)
        div_key=self.teams[team].division
        bb=[]
        for ele in aa:
            for ele2 in self.get_division_team(team):
                if ele2==ele[0]:
                    bb.append(ele)
        if bb[0][0]==team:
##            print('Squad')
##            print(self.teams[team].division)
##            print(team)
            is_leader=True
            return is_leader
        else:
            is_leader=False
        return is_leader

    def div_lead_sort(self,tie,option):
        """This function takes in a league, and takes in the percents, i.e. a list of tuples,
        with the teams as the first tuple element and the win % as the second element of the
        tuple. It then spits out a list containing a list of every team that is tied, in tuple
        form with the first element as the team and the second element as a tuple."""

        #Untested, need to find way to test
        new_order_1=[]
        new_order_2=[]
##        print(tie)
        for team in tie:
            if self.is_division_leader(team[0],option)==True:
                new_order_1.append(team)
                
            else:
                new_order_2.append(team)
##        print('On da block')
##        print(new_order_2)
##        if len(new_order_1)>1:
##            new_order_1=self.h2h_sort(new_order_1,option)
##            
##        if len(new_order_2)>1:
##            new_order_2=self.h2h_sort(new_order_2,option)
##        print('It aint safe')
##        print(new_order_1)

        
        return new_order_1,new_order_2

    def div_won_lost_order(self, teams):
        """takes in a list of teams, and returns a list of the teams in the division, in the order
        of the division standings."""
        real_ps=[]

        percents_div=self.standings(self.get_division_team(teams[0]),conf_merge=False)
        for team_1 in percents:
            for team in teams:
                if team_1[0]==team:
                    real_ps.append(team_1[0])
        return real_ps
                    
        
        


    def split_ties(self,percents):
##        if len(percents)==0:
##            print('Bruh')
        tie_dicto={}
        next_ele_tie=[]
        tie_dicto[percents[0]]=1
        index=0
        index2=0
        empt=[]
        for element in percents:
            index=index+1
            if index==len(percents):
                break
            if percents[index][1]==percents[index-1][1]:
                index2=index2+1
                tie_dicto[percents[index]]=tie_dicto[percents[index-1]]
                empt.append(index+1)
            else:
                    
                tie_dicto[percents[index]]=tie_dicto[percents[index-1]]+1+index2
                index2=0
        flip={}
        for value in tie_dicto.values()+empt:
            flip[value]=[]
        for key in tie_dicto.keys():
            flip[tie_dicto[key]].append(key)
            ties_list=[]

        keys_1=sorted(flip.keys())
        tie_seeds=[]
        for keys in keys_1:
            
            if len(flip[keys])>1:
                ties_list.append(flip[keys])
                new_list=[keys,keys+len(flip[keys])-1]
                tie_seeds.append([keys,keys+len(flip[keys])-1])
        
        return ties_list, tie_seeds
        

    def n_team_sort(self,team_list):
        for team in team_list:
            if self.is_division_leader(team)==True:
                new_order_1.append(tuple(team,1))
            else:
                new_order_2.append(tuple(team,0))
        
        if len(new_order_1)>1:
            new_order_1=self.h2h_sorter(new_order_1,pre_div='False')
            
        if len(new_order_2)>1:
            new_order_2=self.h2h_sorter(new_order_2,pre_div='False')

        

        return new_order_1,new_order_2

        

    def conf_sort(self, percents,option):
        """Takes in a league, a standings i.e. a list of tuples (team, team_record)
        finds the ties, and sorts them into the correct order using conference
        record. It then also checks for ties in conference records and calls the h2h sorter in
        the case of such ties"""
        ties,tie_seeds=self.find_ties(percents)
        if len(ties)==0:
            return percents

        for j in range(len(ties)):
            team_list=[]
            for element in ties[j]:
                team_list.append(element[0])

            conf=self.get_conference(self.teams[team_list[0]].conference)
            
            conf_order= self.standings(conf,option)
            new_order=[]
            for els in conf_order:
                for team in team_list:
                    if team==els[0]:
                        print(team)
                        new_order.append(els)

            if new_order!=self.h2h_sort(new_order,option):
                new_order=self.h2h_sort(new_order,option)
##            
##                
##            if pre_div=True:
##                still_ties=self.find_ties(new_order)
##                
##            if len(still_ties[0])>0:
##                print('DAMN.')
##                print(still_ties)
##            else:
##                print('Grimy')
            tie_teams=[]
            for ele in new_order:
                tie_teams.append((ele[0],ties[j][0][1]))
##            del percents[tie_seeds[j][0]:tie_seeds[j][-1]]
            percents[tie_seeds[j][0]-1:tie_seeds[j][-1]]=tie_teams
        return percents

        
            

            
         

    
        

