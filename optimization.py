import pulp

# To use this module: Must create position amounts (how many players you will consider at each position)
# and player_info array.
# Call setup_data function using these values
# create constraints and find max spending value  
# call optimize function


# range variables: number of players considered at each position
# player_info: 2d array, each element is an array for a position, has (name, salary, projection) info.
# player_info must be in qb,rb,wr,te,d order.
# function returns array of tuples (x,y), x = all player info, y = binary vector. Each tuple is one position
def setup_data(qb_range, rb_range, wr_range, te_range, d_range, player_info):
	# vectors of 0's and 1's, 0 means don't pick, 1 means pick
	qb_vars = pulp.LpVariable.dicts("QB", qb_range, 0, 1, pulp.LpBinary)
	rb_vars = pulp.LpVariable.dicts("RB", rb_range, 0, 1, pulp.LpBinary)
	wr_vars = pulp.LpVariable.dicts("WR", wr_range, 0, 1, pulp.LpBinary)
	te_vars = pulp.LpVariable.dicts("TE", te_range, 0, 1, pulp.LpBinary)
	d_vars = pulp.LpVariable.dicts("D", d_range, 0, 1, pulp.LpBinary)


	player_vars = [qb_vars,rb_vars,wr_vars,te_vars,d_vars]
	player_info_yorn = list(zip(player_info,player_vars))
	return player_info_yorn




def sum(vars):
    return pulp.lpSum(vars)

# q,r,w,t,d,k are 3-tuples with (Name, Cost, Points)
def get_cost(v):
    cost_v = []
    for i in range(len(v)):
        cost= v[i][1]
        cost_v.append(cost)
    return cost_v


def get_points(v):
    points_v = []
    for i in range(len(v)):
        points = v[i][2]
        points_v.append(points)
    return points_v


# returns dot product of binary variable with price/score variable
def dict_dot(normal_v, dict_v):
    sum = 0
    for i in range(len(normal_v)):
        sum += normal_v[i] * pulp.lpSum(dict_v[i])
    return sum


# we want to maximize the sum of the points of our players. "i_vars" is vector of 0's and 1's, parameters are point projections
def objective(player_info_yorn):
	sum = 0
	# calculate the sum of points for all positions
	for i in range(len(player_info_yorn)):
		# dot product of point totals with the binary vector for each position
		sum += dict_dot(get_points(player_info_yorn[i][0]),player_info_yorn[i][1])
	return sum

# total cost of all players has to be less than the max
def constraint1(player_info_yorn):
	sum = 0
	# calculate the sum of cost for all positions
	for i in range(len(player_info_yorn)):
		# dot product of cost totals with the binary vector for each position
		sum += dict_dot(get_cost(player_info_yorn[i][0]), player_info_yorn[i][1])
	return sum


# constraints: array of all constraints to add to the problem
# player_info_yorn: array of tuples (x,y), x = all player info, y = binary vector. Each tuple is one position
# solves the optimzation
def prob_solve(constraints, player_info_yorn,M):
        prob = pulp.LpProblem("BestTeam", pulp.LpMaximize)

        # add the objective function
        prob += objective(player_info_yorn)

        # add the first constraint
        prob += constraint1(player_info_yorn) <= M

        # add all constraints
        for i in range(len(constraints)):
                prob += constraints[i]

        prob.solve()

        return prob
