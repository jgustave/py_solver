from math import exp
from math import log

import numpy as np

from scipy.optimize import minimize, NonlinearConstraint
from numpy import random

#basics learned here:
#https://apmonitor.com/pdc/index.php/Main/NonlinearProgramming

#Equality constraint means that the constraint function result is to be zero whereas inequality means that it is to be NON NEGATIVE
#Constraint Cheat Sheet (how to formulate your constraint function):
# A<=B  becomes B-A
# A=B   becomes B-A
# A>=B  becomes -(B-A)
#Alternately you can just specify the function and pass in limit values using scipy.optimize.NonLinearConstraint  (Way simpler)
#also: https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.NonlinearConstraint.html#scipy.optimize.NonlinearConstraint

#Returns a function that returns clicks given spend.
def make_clicks(intercept1,elasticity1) :
    def click_fn(spend) :
        return exp(intercept1 + (log(spend) * elasticity1 ))
    return click_fn

#Returns a function that returns orders given spend.
#Not sure what cell1 and cell3 are in the original excel doc.
def make_orders(clk_fn,intercept2,elasticity2,cell1,cell3) :
    def orders_fn(spends) :
        return 3.9 * exp(intercept2 + cell1 + cell3 + ( log(clk_fn(spends) ) * elasticity2 ) )
    return orders_fn

#This returns a function that calculates profit given spend. This is our objective function.
def make_profit(order_fn, aov, product_margin) :
    def profit_fn(spends) :
        return (order_fn(spends) * aov * product_margin) - spends
    return profit_fn

def profit_helper(aov,product_margin,intercept1,elasticity1,intercept2,elasticity2,cell1,cell3) :
    return make_profit(make_orders(make_clicks(intercept1,elasticity1),intercept2,elasticity2,cell1,cell3),aov,product_margin)

def make_group_fn(spend_indexes) :
    """
        Make the constraint function that puts a limit on groupings of spend.
    :param spend_indexes: list of indexes that are in the group else all
    :param max_val: The group spend should sum up to <= this
    :return:
    """
    def group_fn(spends) :
        if spend_indexes :
            return sum(spends[spend_indexes])
        else :
            return sum(spends)
    return group_fn

def init_spend(ranges) :
    """
        Given a list of ranges (min,max) for each variable, init an array to a random value in the range.
        This array is the data structure that is used during calculation. the 'spends'
    :param ranges:
    :return: np array
    """
    rands = random.rand(1,len(ranges))[0]
    z = list(zip(ranges,rands))
    n2 = np.array(list(map(lambda tuple: tuple[0][0]+(tuple[0][1]-tuple[0][0])*tuple[1], z)))
    return n2



#Profit for a given category.
prof1 = helper(58.4,0.35,1.24,0.97,0.95,0.49,0.02,0.09)
prof2 = helper(58.4,0.35,1.24,0.97,0.95,0.49,0.02,0.09)
prof3 = helper(58.4,0.35,1.24,0.97,0.95,0.49,0.02,0.09)

#List of Spends (What we are trying to optimize)

spend_bounds=((1,2),(4,6),(10,20))
spends = init_spend(spend_bounds)

#Corresponding list of functions that calculate profit.
profit_fns=[prof1,prof2,prof3]

#Constraints:

#Sum of a specific set(2,3,5) of spends = 1234.5
g1 = NonlinearConstraint(make_group_fn(np.array(2,3,5)), 1234.5, 1234.5)

#Sum of all spends
gall = NonlinearConstraint(make_group_fn(None), 1.0, 1234.5)


#Objective function is sum of profits.
#Given a list of profit functions, and a list of spend variables (That we are optimizing)
#Also, we want to maximize (but python only provides minimize, so flip the sign)
def make_objective(profit_fns):
    def objective_fn(spends) :
        sum_eq = 0.0
        for i in range(0, len(profit_fns)):
            sum_eq = sum_eq + profit_fns[i](spends[i])
        return -sum_eq #flip the sign since we want to maximize
    return objective_fn


# show initial objective
#print('Initial SSE Objective: ' + str(objective(x0)))

cons = ([g1,gall])
objective = make_objective(profit_fns)
solution = minimize(objective,
                    spends,
                    method='SLSQP',
                    bounds=spend_bounds,
                    constraints=cons)
x = solution.x

# show final objective
#print('Final SSE Objective: ' + str(objective(x)))

# print solution
print('Solution')
print('x1 = ' + str(x[0]))
print('x2 = ' + str(x[1]))
print('x3 = ' + str(x[2]))
print('x4 = ' + str(x[3]))
