import package_data as pk
import optimization as op
import table_scrape as ts
import pandas as pd
import sys


# script arguments
salary_file = sys.argv[1]
remove = sys.argv[2]
teams_rm = sys.argv[3]
week = sys.argv[4]


# url to grab projections
qb_url = "https://www.fantasypros.com/nfl/projections/qb.php?week="+str(week)
rb_url = "https://www.fantasypros.com/nfl/projections/rb.php?week="+str(week)
wr_url = "https://www.fantasypros.com/nfl/projections/wr.php?week="+str(week)
te_url = "https://www.fantasypros.com/nfl/projections/te.php?week="+str(week)
d_url = "https://www.fantasypros.com/nfl/projections/dst.php?week="+str(week)

# max you can spend on players
M = 50000

# the number of players at each position we're considering
QB_COUNT= 20
RB_COUNT = 50
WR_COUNT = 50
TE_COUNT = 20
D_COUNT = 20


# df: the dataframe you want to modify
# column: the column name associated with the name of the player
# function: Gets rid of name suffixes (II, III, Jr., Sr.)
def modify_player_names(df, column):
    # the new column to be inserted into the df
    name_array = []

    old_name = df[[column]]
    for i in range(len(old_name)):
        name = old_name.iloc[i].values[0]
        if name.count(' ') > 1:
            first_space_index = name.index(' ')
            snd_space_index = name.index(' ', first_space_index+1)
            name_array.append(name[:snd_space_index])
        else:
            name_array.append(name)

    df[[column]] = name_array





# the binary yorn variables for the optimization setup
qb_yorn = range(QB_COUNT)
rb_yorn = range(RB_COUNT)
wr_yorn = range(WR_COUNT)
te_yorn = range(TE_COUNT)
d_yorn = range(D_COUNT)


position_counts = [QB_COUNT,RB_COUNT, WR_COUNT, TE_COUNT, D_COUNT]



salary_data = pd.read_csv(salary_file)
#DK salary data includes player suffixes, remove them to be able to join data properly
modify_player_names(salary_data,'Name')

qb_projections = ts.qb_projections(qb_url, QB_COUNT, remove, teams_rm)
rb_projections = ts.rb_projections(rb_url, RB_COUNT, remove, teams_rm)
wr_projections = ts.wr_projections(wr_url, WR_COUNT, remove, teams_rm)
te_projections = ts.te_projections(te_url, TE_COUNT, remove, teams_rm)
d_projections = ts.d_projections(d_url, D_COUNT, remove, teams_rm)


position_projections = [qb_projections, rb_projections, wr_projections, te_projections, d_projections]



player_info = pk.package(salary_data,position_projections, position_counts)

player_info_yorn = op.setup_data(qb_yorn, rb_yorn, wr_yorn, te_yorn,d_yorn, player_info)

constraints = []
# we can only have 1 quarterback
constraints.append(op.sum(player_info_yorn[0][1]) == 1)

# we can have at most 3 running backs, must have 2
constraints.append(op.sum(player_info_yorn[1][1]) <= 3)
constraints.append(op.sum(player_info_yorn[1][1]) >= 2)

# we can have at most 4 wide receivers, must have 3
constraints.append(op.sum(player_info_yorn[2][1]) <= 4)
constraints.append(op.sum(player_info_yorn[2][1]) >= 3)

# we can have at most 2 tight ends, must have 1
constraints.append(op.sum(player_info_yorn[3][1]) <= 2)
constraints.append(op.sum(player_info_yorn[3][1]) >= 1)

# we must have 7 running backs, wide receivers, and tight ends combined
constraints.append(op.sum(player_info_yorn[1][1]) + op.sum(player_info_yorn[2][1]) + op.sum(player_info_yorn[3][1]) == 7)

# If we put a rb/wr in flex, we can have at most 6 rb+wr
constraints.append(op.sum(player_info_yorn[1][1])+op.sum(player_info_yorn[2][1])<=6)
#If we put a rb/te in flex, we can have at most 4 rb+te
constraints.append(op.sum(player_info_yorn[1][1])+op.sum(player_info_yorn[3][1])<=4)
#If we put a wr/te in flex, we can have at most 5 wr+te 
constraints.append(op.sum(player_info_yorn[2][1])+op.sum(player_info_yorn[3][1])<=5)


# we need 1 defense
constraints.append(op.sum(player_info_yorn[4][1]) == 1)



# player_info: (name, cost, projection) array for one position
# player_var: yorn array for one position
# function: check if the solver chose a certain position and add the name to the team list
def build_team(player_info, player_var, team):
    for i in player_var:
	    if player_var[i].varValue > 0.00001:
		    name = player_info[i][0]
		    team.append(name)



team = []

op.prob_solve(constraints, player_info_yorn, M)

# look through each position and build the team for every position
for i in range(len(player_info_yorn)):
    build_team(player_info_yorn[i][0], player_info_yorn[i][1], team)

print(team)
