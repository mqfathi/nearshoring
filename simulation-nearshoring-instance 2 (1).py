#!/usr/bin/env python
# coding: utf-8

# In[47]:


import random


# In[48]:


p_l = {}
delta_jl = {}
r_k = {}
d_ij = {}
theta_ml = {}
c_k = {}
beta_ml = {}
epsilon_ml = {}
mu_l = {}
rho_m = {}
q_k_max = {}
h_i1 = {}
h_i={}
pi_m_max = {}
s_m_max = {}
common_jk = {}
e_ijk = {}
varepsilon = {}
varphi = {}
q_k_max = {}
d_m0 = {}

K1 = [1,2,3]
K2 = [4,5,6]
K = K1 + K2
L= [1,2,3]
I = list(range(105))
J = list(range(1, 96))
H = [97, 98, 99, 100, 101, 102, 103, 104]
M = [1,2,3] # Update the value of L to 


for l in L:
    p_l[l] = random.randint(50, 100)  # Assigning random values between 0 and 20
    
for j in J:
    for l in L:
        delta_jl[(j, l)] = random.randint(0, 50)  # Assigning random values between 0 and 20
        
for key in K:
    r_k[key] = random.randint(50, 75)
    
for i in I:
    for j in I:
        if i != j:
            d_ij[(i,j)] = random.randint(1, 15)  # Assigning random values between 0 and 20
        if i == j:
            d_ij[(i,j)] = 0


# In[49]:


d_m0 = {(m, 0): random.randint(1000, 1500) for m in M}

for m in M:
    for l in L:
        theta_ml[(m,l)] = random.randint(20, 45)
        
for k in K:
    c_k[k] =  round(random.uniform(1, 1.5), 1)  # Adjust the range as needed


# In[50]:


for key in K:
    q_k_max[key] = random.randint(200, 500)

for m in M:
    rho_m[m] = random.randint(200, 350)  # Assigning random values between 0 and 20


for l in L:
    mu_l[l] = random.randint(1, 5)  # Assigning random values between 0 and 20


for m in M:
    for l in L:
        beta_ml[(m,l)] = random.randint(10, 20)  # Assigning random values between 0 and 20

for m in M:
    for l in L:
        epsilon_ml[(m,l)] = random.randint(50, 500)  # Assigning random values between 0 and 20


for key in M:
    s_m_max[key] = random.randint(500, 1000)  # Assigning random values between 0 and 20


for idx in I:
    h_i1[idx] = round(random.uniform(1, 25), 2)  # Assigning random values between 3 and 4 (inclusive)


# Divide h_i1 values by 60 to convert minutes to hours
h_i = {key: value / 60 for key, value in h_i1.items()}
    
    
for i in I:
    for j in J:
        for k in K:
            e_ijk[i, j, k] = round(random.uniform(0.3, 1.2), 2)

for j in J:
    for k in K:
        common_jk[(j, k)] = random.randint(15, 75)  # Assigning random values between 0 and 20

f_jlk = {}
for j in J:
    for l in L:
        for k in K:
            f_jlk[j, l, k] = common_jk[j, k]

for key in M:
    pi_m_max[key] = random.randint(500, 1000)  # Assigning random values between 0 and 20

    
    
r_max = round(random.uniform(8, 12), 2)
gamma = random.randint(10, len(J))
Lambda = random.randint(10,len(J))
g_min = random.randint(15000,20000)


varepsilon = round(random.uniform(0.3, 1.2), 2)    # Assigning random values between 0 and 20

# Define Sets and Indice

Omega_jh = {(j, h): 0 for j in J for h in H}

# Calculate the number of customers to assign to hubs (10% of total customers)
num_customers_to_assign = round(len(J) * 0.10)

# Randomly select 10% of customers
customers_to_assign = random.sample(J, num_customers_to_assign)


for j in J:
    if j in customers_to_assign:
        # Randomly choose a hub for this customer
        assigned_hub = random.randint(1, len(H))
        Omega_jh[(j, assigned_hub)] = 1
    else:
        # This customer is not assigned to a hub
        for h in range(1, len(H) + 1):
            Omega_jh[(j, h)] = 0
    
Input = {}
for i in I:
    for i_prime in I:
        if i != i_prime:
            for k in K:
                for j in J:
                    for h in H:
                        Input = c_k[k] * d_ij[i, i_prime] * (1 - Omega_jh.get((j, h), 0))
    
    
for k in K:
    q_k_max[k] = random.uniform(200, 500)     

for i in I:
    varphi[i] = round(random.uniform(0.1, 0.2), 2)    # Assigning random values between 0 and 20


# Update t_ij calculation to include the corrected h_i
# Assuming varphi is applied correctly as a scaling factor for d_ij to time, and h_i adds a fixed service time at node i
t_ij = {key: d_ij[key] * varphi[key[1]] + h_i[key[1]] if key[1] in h_i else d_ij[key] * varphi[key[1]] for key in d_ij}    


# In[51]:


import pulp
import numpy as np

def customer_selection(J, L, K, H, p_l, f_jlk, delta_jl, Omega_jh, Lambda):
    # Initialize decision variable X
    X = {j: 0 for j in J}
    best_profit = -np.inf
    best_X = None
    
    # Initialize an initial solution randomly
    selected_customers = random.sample(J, Lambda)
    for j in selected_customers:
        X[j] = 1
    
    # Calculate the initial profit
    profit = sum(p_l[l] + f_jlk[j, l, k]*(1-Omega_jh[j, h])*delta_jl[j, l] 
                 for j in J for l in L for k in K for h in H if X[j] == 1)
    if profit > best_profit:
        best_profit = profit
        best_X = X.copy()
    
    # Generate all possible combinations of (0,1) in X
    for j in J:
        X_temp = X.copy()
        X_temp[j] = 1 - X_temp[j]  # Toggle the selection of customer j
        profit_temp = sum(p_l[l] + f_jlk[j, l, k]*(1-Omega_jh[j, h])*delta_jl[j, l] 
                          for j in J for l in L for k in K for h in H if X_temp[j] == 1)
        
        # If the new profit is better, update best_X and best_profit
        if profit_temp > best_profit:
            best_profit = profit_temp
            best_X = X_temp.copy()
    
    return best_X


# In[52]:


best_X = customer_selection(J, L, K, H, p_l, f_jlk, delta_jl, Omega_jh, Lambda)


# In[53]:


import pulp

def manufacturing_facility_selection_and_production_assignment(X, M, L, J, beta_ml, rho_m, epsilon_ml, mu_l, delta_jl, s_m_max, pi_m_max):
    V = set()
    U = {(m, l): 0 for m in M for l in L}  # Initialize production quantity as zero
    
    # Initialize the problem
    follower_problem = pulp.LpProblem("Manufacturing_Facility_Selection", pulp.LpMinimize)
    
    # Define decision variables for production quantities and plant selection
    u = pulp.LpVariable.dicts("production_quantity", ((m, l) for m in M for l in L), lowBound=0, cat='Continuous')
    v = pulp.LpVariable.dicts("plant_selection", (m for m in M), cat='Binary')
    
    # Calculate consolidated demand for each commodity based on selected customers
    consolidated_demand = {l: sum(delta_jl[j, l] for j in J if X[j] == 1) for l in L}
    
    # Simplified version: Assign all production to the plant with the lowest beta_ml + rho_m for each l
    for l in L:
        min_cost_plant = min(M, key=lambda m: beta_ml[m, l] + rho_m[m])
        U[min_cost_plant, l] = consolidated_demand[l]
        V.add(min_cost_plant)
    
    # Constraints
    # Carbon emissions constraint
    for m in M:
        follower_problem += pulp.lpSum(epsilon_ml[m, l] * u[(m, l)] for l in L) <= s_m_max[m], f"CarbonEmission_{m}"
    
    # Demand satisfaction constraint (assuming your demand calculation matches production)
    for l in L:
        follower_problem += pulp.lpSum(u[(m, l)] for m in M) == consolidated_demand[l], f"DemandSatisfaction_{l}"
    
    # Raw material constraint
    for m in M:
        follower_problem += pulp.lpSum(mu_l[l] * u[(m, l)] for l in L) <= pi_m_max[m] * v[m], f"RawMaterial_{m}"
    
    # Note: This corrected version assumes the decision variables `u` and `v` are properly integrated into your model
    # and that `follower_problem` is where you're adding your constraints and objective.
    
    # You should define an objective for your `follower_problem` and solve it using follower_problem.solve().
    
    return V, U


# In[54]:



V, U = manufacturing_facility_selection_and_production_assignment(best_X, M, L, J, beta_ml, rho_m, epsilon_ml, mu_l, delta_jl, s_m_max, pi_m_max)

V_dict = {m: (1 if m in V else 0) for m in M}


# In[55]:


def determine_customer_hub(Omega_jh, H):
    """
    Determine the hub selected by each customer based on Omega_jh.
    Parameters:
    - Omega_jh: Dictionary with keys as (j, h) and values indicating selection (1 or 0).
    - H: List of hubs.
    
    Returns:
    - customer_to_hub: Dictionary mapping each customer to their chosen hub location.
    """
    customer_to_hub = {}
    for (j, h), selection in Omega_jh.items():
        if selection == 1:
            customer_to_hub[j] = h
    return customer_to_hub


# In[56]:


def calculate_savings(I, d_ij, x, Omega_jh, H):
    """
    Calculate savings for combining two selected customers, considering hub assignments.
    Parameters:
    - I: Set including customers and hubs.
    - d_ij: Distance matrix.
    - x: Dictionary indicating whether a customer is selected (1) or not (0).
    - Omega_jh: Customer preferences for hubs.
    - H: List of hubs.
    """
    customer_to_hub = determine_customer_hub(Omega_jh, H)  # Determine hubs for customers
    savings = {}
    for i in I:
        location_i = customer_to_hub.get(i, i)  # Use hub's location if customer chose a hub, else use customer's location

        for j in I:
            location_j = customer_to_hub.get(j, j)  # Same for customer j

            if i != j and i > 0 and j > 0 and x.get(i, 0) == 1 and x.get(j, 0) == 1:  # Only consider selected customers
                savings[(i, j)] = d_ij[(0, location_i)] + d_ij[(0, location_j)] - d_ij[(location_i, location_j)]
    return savings


# In[57]:


def calculate_total_demand_per_customer(delta_jl, J, L):
    """Calculate total demand for each customer across all commodities."""
    total_demand_per_customer = {j: sum(delta_jl.get((j, l), 0) for l in L) for j in J}
    return total_demand_per_customer


# In[58]:


def vehicle_routing_assignment_with_time_constraint(I, J, K, d_ij, q_k_max, L, delta_jl, x, u, v, Omega_jh, H, t_ij, r_max):
    # Calculate total demand for each customer
    total_demand_per_customer = calculate_total_demand_per_customer(delta_jl, J, L)
    
    # Initialize structures for routing with time consideration
    routes = {k: [] for k in K}
    load = {k: 0 for k in K}
    time_spent = {k: 0 for k in K}  # Initialize time spent on each route
    used_vehicles = set()
    customer_route = {j: None for j in J if x[j] == 1}  # Only consider selected customers

    # Calculate savings with consideration for customer selection and hub assignments
    savings = calculate_savings(I, d_ij, x, Omega_jh, H)
    sorted_savings = sorted(savings.items(), key=lambda x: x[1], reverse=True)

    # Assign routes based on savings, vehicle capacity, and time constraints
    for (i, j), saving in sorted_savings:
        for k in K:
            if customer_route[i] is None and customer_route[j] is None:
                total_demand_i = total_demand_per_customer.get(i, 0)
                total_demand_j = total_demand_per_customer.get(j, 0)
                if load[k] + total_demand_i + total_demand_j <= q_k_max[k]:
                    # Check if adding these customers respects the time constraint
                    additional_time = t_ij.get((0, i), 0) + t_ij.get((i, j), 0) + t_ij.get((j, 0), 0)
                    if time_spent[k] + additional_time <= r_max:
                        routes[k].append(i)
                        routes[k].append(j)
                        load[k] += total_demand_i + total_demand_j
                        time_spent[k] += additional_time
                        customer_route[i] = k
                        customer_route[j] = k
                        used_vehicles.add(k)
                        break  # Vehicle found for the pair

    # Attempt to add remaining selected customers to existing routes, considering time
    for j in J:
        if x[j] == 1 and customer_route[j] is None:
            total_demand_j = total_demand_per_customer.get(j, 0)
            for k in K:
                if load[k] + total_demand_j <= q_k_max[k]:
                    # Check time constraint for adding this customer
                    additional_time = t_ij.get((0, j), 0) + t_ij.get((j, 0), 0)
                    if time_spent[k] + additional_time <= r_max:
                        routes[k].append(j)
                        load[k] += total_demand_j
                        time_spent[k] += additional_time
                        customer_route[j] = k
                        used_vehicles.add(k)
                        break

    # Report if any selected customers could not be assigned
    unassigned_customers = [j for j, route in customer_route.items() if route is None]
    if unassigned_customers:
        print(f"Warning: Not all selected customers could be assigned to routes. Unassigned customers: {unassigned_customers}")

    return routes, used_vehicles


# In[59]:


def enhanced_routing_output(routes, customer_to_hub):
    """
    Enhance the routing output to include information about hub assignments for customers.
    
    Parameters:
    - routes: Dictionary of routes per vehicle.
    - customer_to_hub: Dictionary mapping customers to their chosen hub.
    
    Returns:
    - A dictionary with detailed routing information including hub assignments.
    """
    detailed_routes = {}
    for k, route in routes.items():
        route_details = []
        for customer_or_hub in route:
            if customer_or_hub in customer_to_hub:
                # Customer is assigned to a hub
                hub = customer_to_hub[customer_or_hub]
                route_details.append({'customer': customer_or_hub, 'hub': hub})
            else:
                # Direct delivery to customer or a hub itself
                route_details.append({'direct': customer_or_hub})
        detailed_routes[k] = route_details
    
    return detailed_routes


# In[60]:


customer_to_hub = determine_customer_hub(Omega_jh, H)


# In[61]:


def generate_initial_solution():
    # Step 1: Customer selection
    X = customer_selection(J, L, K, H, p_l, f_jlk, delta_jl, Omega_jh, Lambda)
    
    # Step 2: Manufacturing facility selection and production assignment
    V, U = manufacturing_facility_selection_and_production_assignment(X, M, L, J, beta_ml, rho_m, epsilon_ml, mu_l, delta_jl, s_m_max, pi_m_max)
    
    # Convert set V to dict for compatibility
    V_dict = {m: (1 if m in V else 0) for m in M}
    
    # Step 3: Vehicle routing assignment with time constraint
    routes, used_vehicles_set = vehicle_routing_assignment_with_time_constraint(I, J, K, d_ij, q_k_max, L, delta_jl, X, U, V_dict, Omega_jh, H, t_ij, r_max)
    
    used_vehicles = {k: 1 if k in used_vehicles_set else 0 for k in K}

    
    manufacturing_costs = calculate_follower_objective(M, L, beta_ml, rho_m, U, V_dict)
    profit = calculate_profit(I, J, H, K, L, M, p_l, f_jlk, delta_jl, Omega_jh, r_k, routes, c_k, theta_ml, U, X, used_vehicles)
    emissions = calculate_emissions(I, K, M, L, e_ijk, d_ij, routes, epsilon_ml, U, varepsilon, d_m0, V_dict)
    
    
    # Combine all parts of the solution
    initial_solution = {
        'x': X,
        'v': V_dict,
        'u': U,
        'y': routes,
        'z': used_vehicles,
        
        # Initial objective values can be calculated based on the initial decision variables
        "emissions_value": emissions,
        "profit_value": profit,
        "follower_objective": manufacturing_costs
    }
    
    return initial_solution


# In[62]:


def extract_objective_values(solutions, I, J, H, K, L, M, e_ijk, d_ij, epsilon_ml, varepsilon, d_m0, p_l, f_jlk, delta_jl, Omega_jh, r_k, c_k, theta_ml, beta_ml, rho_m):
    solutions_list = [solutions]
    objective_values = {'L_emissions': [], 'surrogate_objective' : [], 'follower_objective': []}
    
    for solution in solutions_list:
        # Decompose the solution into its components
        y = solution['y']
        u = solution['u']
        v = solution['v']
        x = solution['x']
        z = solution['z']

        # Calculate each objective value
        emissions_value = calculate_emissions(I, K, M, L, e_ijk, d_ij, y, epsilon_ml, u, varepsilon, d_m0, v)
        #profit_value = calculate_profit(I, J, H, K, L, M, p_l, f_jlk, delta_jl, Omega_jh, r_k, y, c_k, theta_ml, u, x, z)
        follower_value = calculate_follower_objective(M, L, beta_ml, rho_m, u, v)
        profit_surrogate = calculate_profit_surrogate(I, J, H, K, L, M, p_l, f_jlk, delta_jl, Omega_jh, r_k, y, c_k, theta_ml, u, x, z)

        # Append the calculated values to the respective lists in the dictionary
        objective_values['L_emissions'].append(emissions_value)
        #objective_values['L_profit'].append(profit_value)
        objective_values['surrogate_objective'].append(profit_surrogate)
        objective_values['follower_objective'].append(follower_value)
    
    return objective_values


def calculate_emissions(I, K, M, L, e_ijk, d_ij, y, epsilon_ml, u, varepsilon, d_m0, v):
    emissions = 0
    # Sum emissions for transportation
    for i in I:
        for i_prime in I:
            if i != i_prime:
                for k in K:
                    e_value = e_ijk.get((i, i_prime, k), 0)
                    d_value = d_ij.get((i, i_prime), 0)
                    y_value = y.get((i, i_prime, k), 0)
                    emissions += e_value * d_value * y_value
    # Sum emissions for manufacturing
    for m in M:
        for l in L:
            epsilon_value = epsilon_ml.get((m, l), 0)  # Default to 0 if not found
            u_value = u.get((m, l), 0)  # Default to 0 if not found
            emissions += epsilon_value * u_value
            
    # Sum emissions for transporting goods from manufacturing to depot
    for m in M:
        d_m0_value = d_m0.get((m, 0), 0)
        emissions += varepsilon * d_m0_value * v.get(m, 0)

    return emissions


def calculate_profit(I, J, H, K, L, M, p_l, f_jlk, delta_jl, Omega_jh, r_k, y, c_k, theta_ml, u, x, Z):
    profit = 0
    z = {vehicle_id: 1 for vehicle_id in Z}
    # Revenue from sales and delivery fees, adjusted for customer preferences for delivery mode
    for j in J:
        for l in L:
            for k in K:
                # Iterate over all H values
                for h in H:
                    # Safely get the value from f_jlk with a default of 0
                    f_jlk_value = f_jlk.get((j, l, k), 0)
                    # Calculate the profit contribution for this j, l, k combination
                    profit_contribution = (p_l[l] + f_jlk_value * (1 - Omega_jh.get((j, h), 0))) * delta_jl[j, l] * x[j]
                    profit += profit_contribution
    # Deduct costs for vehicle use
    for k in K:
        profit -= r_k[k] * z[k]
    # Deduct transportation costs, adjusted for delivery mode preference and actual route usage
    for i in I:
        for i_prime in I:
            if i != i_prime:
                for k in K:
                    for j in J:
                        for h in H:
                            profit -= c_k[k] * d_ij[i, i_prime] * y.get((i, i_prime, k), 0) * (1 - Omega_jh.get((j, h), 0))
    # Deduct manufacturing costs
    for m in M:
        for l in L:
            profit -= theta_ml[m, l] * u[m, l]
    return profit


def calculate_follower_objective(M, L, beta_ml, rho_m, u, v):
    # Manufacturing cost minimization objective
    manufacturing_costs = 0
    for m in M:
        for l in L:
            manufacturing_costs += beta_ml[m, l] * u.get((m, l), 0)
        manufacturing_costs += rho_m[m] * v.get(m, 0)

    return manufacturing_costs





# In[63]:


def calculate_profit_surrogate(I, J, H, K, L, M, p_l, f_jlk, delta_jl, Omega_jh, r_k, y, c_k, theta_ml, u, x, Z):
    profit = 0
    z = {vehicle_id: 1 for vehicle_id in Z}
    average_cost = sum(c_k.values()) / len(c_k)
    # Calculate the average of d_ij values excluding the diagonal (i == j)
    sum_distances = sum(d_ij.values())  # Sum of all distances
    num_distances = len([d for d in d_ij.values() if d != 0])  # Number of non-zero distances

    # Calculate average distance
    average_distance = sum_distances / num_distances if num_distances else 0
    # Revenue from sales and delivery fees, adjusted for customer preferences for delivery mode
    for j in J:
        for l in L:
            for k in K:
                # Iterate over all H values
                for h in H:
                    # Safely get the value from f_jlk with a default of 0
                    f_jlk_value = f_jlk.get((j, l, k), 0)
                    # Calculate the profit contribution for this j, l, k combination
                    profit_contribution = (p_l[l] + f_jlk_value * (1 - Omega_jh.get((j, h), 0))) * delta_jl[j, l] * x[j]
                    profit += profit_contribution
    # Deduct costs for vehicle use
    for k in K:
        profit -= r_k[k] * z[k]
    # Deduct transportation costs, adjusted for delivery mode preference and actual route usage
    #for i in I:
    #    for i_prime in I:
    #        if i != i_prime:
    #            for k in K:
    #                tempt = average_cost * average_distance * y.get((i, i_prime, k), 0)
    #                for j in J:
    #                    for h in H:
    #                        profit -= tempt * (1 - Omega_jh.get((j, h), 0))    # Deduct manufacturing costs
                            
    for k in K:
        for i in J:  # Iterate over customers
            for j in J:  # Iterate over customers for customer-to-customer distances
                if Omega_jh.get((j, h), 0) == 0:
                    profit -= c_k[k] * d_ij[i, i_prime] * y.get((i, j, k), 0)
                # Further calculations or storing results as needed

            for h_index, h in enumerate(H, start=len(J)+1):  # Iterate over hubs for customer-to-hub distances
                if Omega_jh.get((i, h), 0) == 1:
                    profit -= c_k[k] * d_ij[i, i_prime] * y.get((i, h_index, k), 0)
                # Further calculations or storing results as needed
    for m in M:
        for l in L:
            profit -= theta_ml[m, l] * u[m, l]
    return profit


# In[ ]:


for b in range(30):
    solutions = generate_initial_solution()
    final = extract_objective_values(solutions, I, J, H, K, L, M, e_ijk, d_ij, epsilon_ml, varepsilon, d_m0, p_l, f_jlk, delta_jl, Omega_jh, r_k, c_k, theta_ml, beta_ml, rho_m)
    print(f"Run {1+b}: {final}")


# In[21]:


Omega_jh


# In[ ]:




