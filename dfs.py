import pulp


# max you can spend on players
M = 78


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

def dict_dot(normal_v,dict_v):
    sum = 0
    for i in range(len(normal_v)):
        sum += normal_v[i] * pulp.lpSum(dict_v[i])
    return sum




# the number of players at each position we're considering
qb_amount = range(32)
rb_amount = range(50)
wr_amount = range(50)
te_amount = range(32)
d_amount = range(32)
k_amount = range(32)


# vectors of 0's and 1's, 0 means don't pick, 1 means pick
q_vars = pulp.LpVariable.dicts("QB", qb_amount, 0, 1, pulp.LpBinary)
r_vars = pulp.LpVariable.dicts("RB", rb_amount, 0, 1, pulp.LpBinary)
w_vars = pulp.LpVariable.dicts("WR", wr_amount, 0, 1, pulp.LpBinary)
t_vars = pulp.LpVariable.dicts("TE", te_amount, 0, 1, pulp.LpBinary)
d_vars = pulp.LpVariable.dicts("D", d_amount, 0, 1, pulp.LpBinary)
k_vars = pulp.LpVariable.dicts("K", k_amount, 0, 1, pulp.LpBinary)


# scrape data, return 3-tuple vectors of q,r,w,t,d,k




# we want to maximize the sum of the points of our players. "i_vars" is vector of 0's and 1's, parameters are point projections
def objective(q,r,w,t,d,k):
    return dict_dot(get_points(q),q_vars) + dict_dot(get_points(r),r_vars) + dict_dot(get_points(w),w_vars) + dict_dot(get_points(t),t_vars) + dict_dot(get_points(d),d_vars) + dict_dot(get_points(k),k_vars)

# total cost of all players has to be less than the max
def constraint1(q,r,w,t,d,k):
    q_cost = dict_dot(get_cost(q), q_vars)
    r_cost = dict_dot(get_cost(r), r_vars)
    w_cost = dict_dot(get_cost(w), w_vars)
    t_cost = dict_dot(get_cost(t), t_vars)
    d_cost = dict_dot(get_cost(d), d_vars)
    k_cost = dict_dot(get_cost(k), k_vars)
    return q_cost + r_cost + w_cost + t_cost + d_cost + k_cost




prob = pulp.LpProblem("BestTeam", pulp.LpMaximize)

# add the objective function
prob += objective(q,r,w,t,d,k)

# add the first constraint
prob += constraint1(q,r,w,t,d,k) <= M

# we can only have 1 quarterback
prob += pulp.lpSum(q_vars) == 1

# we can have at most 3 running backs, must have 2
prob += pulp.lpSum(r_vars) <= 3
prob += pulp.lpSum(r_vars) >= 2

# we can have at most 3 wide receivers, must have 2
prob += pulp.lpSum(w_vars) <= 3
prob += pulp.lpSum(w_vars) >= 2

# we can have at most 2 tight ends, must have 1
prob += pulp.lpSum(t_vars) <= 2
prob += pulp.lpSum(t_vars) >= 1


# we must have 6 running backs, wide receivers, and tight ends combined
prob += pulp.lpSum(r_vars) + pulp.lpSum(w_vars) + pulp.lpSum(t_vars) == 6

# we need 1 defense
prob += pulp.lpSum(d_vars) == 1

# we need 1 kicker
prob += pulp.lpSum(k_vars) == 1


prob.solve()


# recommended team
Team = []

# get recommended qb
for i in q_vars:
    if q_vars[i].varValue > 0.00001:
        name, cost, points = q[i]
        Team.append(name)

# get recommended rb
for i in r_vars:
    if r_vars[i].varValue > 0.00001:
        name, cost, points = r[i]
        Team.append(name)

# get recommended wr
for i in w_vars:
    if w_vars[i].varValue > 0.00001:
        name, cost, points = w[i]
        Team.append(name)

# get recommended te
for i in t_vars:
    if t_vars[i].varValue > 0.00001:
        name, cost, points = t[i]
        Team.append(name)

# get recommended defense
for i in d_vars:
    if d_vars[i].varValue > 0.00001:
        name, cost, points = d[i]
        Team.append(name)

# get recommended kicker
for i in k_vars:
    if k_vars[i].varValue > 0.00001:
        name, cost, points = k[i]
        Team.append(name)

print(Team)
