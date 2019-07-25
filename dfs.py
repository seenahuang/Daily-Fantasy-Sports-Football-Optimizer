import pulp

# max you can spend on players
M = 78

# the number of players at each position we're considering
QB_AMOUNT = range(32)
RB_AMOUNT = range(50)
WR_AMOUNT = range(50)
TE_AMOUNT = range(32)
D_AMOUNT = range(32)
K_AMOUNT = range(32)

# vectors of 0's and 1's, 0 means don't pick, 1 means pick
Q_VARS = pulp.LpVariable.dicts("QB", QB_AMOUNT, 0, 1, pulp.LpBinary)
R_VARS = pulp.LpVariable.dicts("RB", RB_AMOUNT, 0, 1, pulp.LpBinary)
W_VARS = pulp.LpVariable.dicts("WR", WR_AMOUNT, 0, 1, pulp.LpBinary)
T_VARS = pulp.LpVariable.dicts("TE", TE_AMOUNT, 0, 1, pulp.LpBinary)
D_VARS = pulp.LpVariable.dicts("D", D_AMOUNT, 0, 1, pulp.LpBinary)
K_VARS = pulp.LpVariable.dicts("K", K_AMOUNT, 0, 1, pulp.LpBinary)

# Building team iteratively. 
PLAYER_VARS = [Q_VARS,R_VARS,W_VARS,T_VARS,D_VARS,K_VARS]
PLAYERS = [q, r, w, t, d, k]

# recommended team
Team = []

# q,r,w,t,d,k are 3-tuples with (Name, Cost, Points)
def get_cost(v):
    cost_v = []
    for i in range(len(v)):
        name, cost, points = v[i]
        cost_v.append(cost)
    return cost_v


def get_points(v):
    points_v = []
    for i in range(len(v)):
        name, cost, points = v[i]
        points_v.append(points)
    return points_v


def dict_dot(normal_v, dict_v):
    sum = 0
    for i in range(len(normal_v)):
        sum += normal_v[i] * pulp.lpSum(dict_v[i])
    return sum

# scrape data, return 3-tuple vectors of q,r,w,t,d,k (from other module)

# we want to maximize the sum of the points of our players. "i_vars" is vector of 0's and 1's, parameters are point projections
def objective(q, r, w, t, d, k):
    return dict_dot(get_points(q), Q_VARS) + dict_dot(get_points(r), R_VARS) + dict_dot(get_points(w), W_VARS) + dict_dot(get_points(t), T_VARS) + dict_dot(get_points(d), D_VARS) + dict_dot(get_points(k), K_VARS)

# total cost of all players has to be less than the max
def constraint1(q, r, w, t, d, k):
    q_cost = dict_dot(get_cost(q), Q_VARS)
    r_cost = dict_dot(get_cost(r), R_VARS)
    w_cost = dict_dot(get_cost(w), W_VARS)
    t_cost = dict_dot(get_cost(t), T_VARS)
    d_cost = dict_dot(get_cost(d), D_VARS)
    k_cost = dict_dot(get_cost(k), K_VARS)
    return q_cost + r_cost + w_cost + t_cost + d_cost + k_cost

# Possible scope issue may need to pass objective and constraint1 functions to call properly. 
def prob_setup():
        prob = pulp.LpProblem("BestTeam", pulp.LpMaximize)

        # add the objective function
        prob += objective(q, r, w, t, d, k)

        # add the first constraint
        prob += constraint1(q, r, w, t, d, k) <= M

        # we can only have 1 quarterback
        prob += pulp.lpSum(Q_VARS) == 1

        # we can have at most 3 running backs, must have 2
        prob += pulp.lpSum(R_VARS) <= 3
        prob += pulp.lpSum(R_VARS) >= 2

        # we can have at most 3 wide receivers, must have 2
        prob += pulp.lpSum(W_VARS) <= 3
        prob += pulp.lpSum(W_VARS) >= 2

        # we can have at most 2 tight ends, must have 1
        prob += pulp.lpSum(T_VARS) <= 2
        prob += pulp.lpSum(T_VARS) >= 1

        # we must have 6 running backs, wide receivers, and tight ends combined
        prob += pulp.lpSum(R_VARS) + pulp.lpSum(W_VARS) + pulp.lpSum(T_VARS) == 6

        # we need 1 defense
        prob += pulp.lpSum(D_VARS) == 1

        # we need 1 kicker
        prob += pulp.lpSum(K_VARS) == 1

        prob.solve()

        return prob

def build_team(player_var, player):
        for i in player_var:
                if player_var[i].varValue > 0.00001:
                        name, cost, points = player[i]
                        Team.append(name)
def main():
        prob_setup()
        for player_var in PLAYER_VARS:
                for player in PLAYERS:
                        build_team(player_var, player)
        print(Team)

if __name__ == "__main__":
    main()