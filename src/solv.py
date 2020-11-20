from math import exp
from math import log

import numpy as np

from scipy.optimize import minimize

#basics learned here:
#https://apmonitor.com/pdc/index.php/Main/NonlinearProgramming

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

#This returns a function that calculates profit given spend. This is our objective function.
def make_profit(order_fn, aov, product_margin) :
    def profit_fn(spend) :
        return (order_fn(spend) * aov * product_margin) - spend
    return profit_fn

#EXAMPLE. Create and profit function and evaluate with spend=10
#prof = make_profit(make_orders(make_clicks(1.24,0.97),0.95,0.49,0.02,0.09),58.4,0.35)
#spend=10
#prof(spend)

#List of Spends (What we are trying to optimize)
spends=np.zeros(3)
spends[0]=1.0
spends[2]=11.0
spends[3]=7.0

#Corresponding list of functions that calculate profit.
profit_fns=[]

#Objective function is sum of profits.
#Given a list of profit functions, and a list of spend variables (That we are optimizing)
def objective(profit_fns,spends):
    sum_eq = 0.0
    for i in range(0, len(profit_fns)):
        sum_eq = sum_eq + profit_fns[i](spends[i])
    return sum_eq



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
