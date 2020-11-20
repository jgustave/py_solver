from math import exp
from math import log

import numpy as np

from scipy.optimize import minimize

#basics learned here:
#https://apmonitor.com/pdc/index.php/Main/NonlinearProgramming

# We want to maximize the sum of several functions
# First lets make a function that returns a partial function
#test


#Returns a function that returns clicks given spend.
def make_clicks(intercept1,elasticity1) :
    def click_fn(spend) :
        return exp(intercept1 + (log(spend) * elasticity1 ))
    return click_fn

#Returns a function that returns orders given spend.
#Not sure what cell1 and cell3 are in the original excel doc.
def make_orders(clk_fn,intercept2,elasticity2,cell1,cell3) :
    def orders_fn(spend) :
        return 3.9 * exp(intercept2 + cell1 + cell3 + ( log(clk_fn(spend) ) * elasticity2 ) )
    return orders_fn

def make_profit(order_fn, aov, product_margin) :
    def profit_fn(spend) :
        return (order_fn(spend) * aov * product_margin) - spend
    return profit_fn




#Objective function is sum of partials.
def objective(partials):
    return partials[0]*partials[3]*(partials[0]+partials[1]+partials[2])+partials[2]


def constraint1(x):
    return x[0]*x[1]*x[2]*x[3]-25.0

def constraint2(x):
    sum_eq = 40.0
    for i in range(4):
        sum_eq = sum_eq - x[i]**2
    return sum_eq

# initial guesses
n = 4
x0 = np.zeros(n)
x0[0] = 1.0
x0[1] = 5.0
x0[2] = 5.0
x0[3] = 1.0

# show initial objective
print('Initial SSE Objective: ' + str(objective(x0)))

# optimize
b = (1.0,5.0)
bnds = (b, b, b, b)
con1 = {'type': 'ineq', 'fun': constraint1}
con2 = {'type': 'eq', 'fun': constraint2}
cons = ([con1,con2])
solution = minimize(objective,x0,method='SLSQP',bounds=bnds,constraints=cons)
x = solution.x

# show final objective
print('Final SSE Objective: ' + str(objective(x)))

# print solution
print('Solution')
print('x1 = ' + str(x[0]))
print('x2 = ' + str(x[1]))
print('x3 = ' + str(x[2]))
print('x4 = ' + str(x[3]))
