from math import exp
from math import log
from scipy.optimize import minimize, NonlinearConstraint
from numpy import random
import numpy as np


#AOV,ProductMargin.InterceptS1,ElasticityS1,InterceptS2,ElasticityS2,Cell1,Cell3,MaxSpend,MinSpend
demo_data=(
(58.398254103185,0.350000000000,1.240958573018,0.972529086443,0.947600000000,0.485600000000,0.017500000000,0.091200000000,2678.112413793100,223.176034482759),
(61.860509649813,0.350000000000,2.824050392671,0.701792889806,1.273900000000,0.497500000000,0.010600000000,0.171100000000,19220.313103448300,1601.692758620690),
(64.868840885516,0.350000000000,2.765981178645,0.592331961459,0.507300000000,0.311000000000,-0.028300000000,0.290900000000,6178.235172413790,514.852931034483),
(57.055295826294,0.350000000000,2.616352828903,0.793574991918,0.962800000000,0.374000000000,-0.160000000000,0.201300000000,34214.201379310300,2851.183448275860),
(53.339351098952,0.350000000000,3.459025959398,0.639025558378,0.700200000000,0.401300000000,-0.040000000000,0.220400000000,15668.333793103500,1305.694482758620),
(57.141460576909,0.350000000000,3.109883143990,0.637343349177,0.313700000000,0.342500000000,-0.257900000000,0.109100000000,4569.748965517240,380.812413793103),
(54.303740674486,0.350000000000,2.802426933379,0.705420443934,-0.006200000000,0.498300000000,-0.215500000000,0.034900000000,35291.178620689700,2940.931551724140),
(58.207317015877,0.350000000000,2.368526776965,0.801904503936,0.185000000000,0.340400000000,-0.187300000000,0.068300000000,121892.886206897000,10157.740517241400),
(45.866035481002,0.350000000000,1.850779610802,0.826975638316,0.567300000000,0.356300000000,-0.136000000000,0.250100000000,29369.933793103400,2447.494482758620),
(61.091147332545,0.350000000000,1.572153431275,0.841809663771,0.772800000000,0.402800000000,-0.127900000000,0.108000000000,6427.555862068970,535.629655172414),
(61.832525462645,0.350000000000,2.366966342046,0.650404032434,0.486400000000,0.392200000000,-0.105600000000,0.145500000000,921.386896551724,76.782241379310),
(69.123493975904,0.350000000000,1.458999858048,0.734114878832,0.796100000000,0.444900000000,0.067800000000,0.212500000000,765.529655172414,63.794137931035),
(54.582053560097,0.350000000000,3.445394224353,0.629658972765,0.514600000000,0.365300000000,-0.119700000000,0.205000000000,2754.782068965510,229.565172413793),
(63.363514362886,0.350000000000,3.105644046298,0.659563081967,-2.087600000000,0.836600000000,-0.270900000000,-0.346500000000,5639.108275862070,469.925689655172),
(68.766321623604,0.350000000000,1.957505168968,0.763021738184,0.456500000000,0.359400000000,-0.325900000000,0.086800000000,3783.388965517240,315.282413793103),
(62.088997140739,0.350000000000,1.838232507764,0.805126690512,-0.097600000000,0.499600000000,0.058900000000,0.037300000000,5498.176551724140,458.181379310345),
(59.033682968590,0.350000000000,2.414406163328,0.681268789615,0.061300000000,0.288400000000,-0.280600000000,-0.048700000000,1742.085517241380,145.173793103448),
(66.366872984693,0.350000000000,2.034724730917,0.693761030828,-0.474100000000,0.437100000000,-0.296100000000,-0.201700000000,3263.333793103450,271.944482758621),
(58.267377535477,0.350000000000,3.582341459301,0.598611730154,0.679900000000,0.408600000000,-0.186200000000,0.113600000000,2549.025517241380,212.418793103448),
(64.020685449445,0.350000000000,2.144822372282,0.782768983780,0.398100000000,0.376800000000,-0.134600000000,0.107700000000,1407.103448275860,117.258620689655),
(57.989568256752,0.350000000000,3.111560995503,0.681619772176,0.651400000000,0.408800000000,-0.302400000000,0.133400000000,5960.908965517240,496.742413793103),
(62.677089130078,0.350000000000,2.259706266347,0.761997339858,0.554900000000,0.394400000000,-0.213200000000,-0.019900000000,9581.627586206900,798.468965517242),
(49.109576291942,0.350000000000,1.525173011762,0.867551185288,1.445800000000,0.453000000000,-0.102500000000,0.066600000000,2434.460689655170,202.871724137931),
(57.996962922344,0.350000000000,2.954453407024,0.618675670867,-0.389700000000,0.364600000000,0.010300000000,0.143300000000,2625.984827586210,218.832068965517),
(67.103518146607,0.350000000000,2.313515823579,0.655115088907,0.152400000000,0.391600000000,-0.224800000000,0.176900000000,3567.986896551720,297.332241379310),
(48.445671806536,0.350000000000,3.694874632150,0.636428644057,0.135800000000,0.392800000000,-0.177700000000,0.285800000000,5615.745517241380,467.978793103448),
(53.560166822212,0.350000000000,3.153453719239,0.629555982011,-1.193600000000,0.481400000000,0.092300000000,0.211700000000,2975.228275862070,247.935689655172),
(49.302847489449,0.350000000000,3.424992607444,0.659565052463,0.462600000000,0.371800000000,-0.172100000000,0.171300000000,14352.246206896600,1196.020517241380),
(58.647357052967,0.350000000000,2.231210790520,0.755136276796,-0.866000000000,0.383300000000,-0.167500000000,-0.009700000000,8588.548965517240,715.712413793104),
(44.471020100403,0.350000000000,1.931106245018,0.784413621055,0.103200000000,0.356300000000,-0.092000000000,0.119100000000,8496.473793103450,708.039482758621),
(57.390083965848,0.350000000000,2.954129501883,0.615910575646,-0.140500000000,0.378100000000,-0.310800000000,0.059900000000,2467.909655172410,205.659137931035),
(62.475190741092,0.350000000000,2.205648259574,0.688278790005,0.876000000000,0.376000000000,0.018600000000,0.244600000000,5089.282758620690,424.106896551724),
(51.727110769715,0.350000000000,3.500757838547,0.666830521277,1.013800000000,0.441200000000,-0.009700000000,0.184100000000,5431.994482758630,452.666206896552),
(56.854688316970,0.350000000000,2.870487680961,0.696498414884,-0.699500000000,0.343800000000,-0.051200000000,-0.066800000000,4032.095172413790,336.007931034483),
(49.035715733434,0.350000000000,3.626727467893,0.652872207539,-0.187400000000,0.392200000000,0.072300000000,0.189800000000,17158.334482758600,1429.861206896550),
(58.236038776147,0.350000000000,2.412001798323,0.754925264061,-0.595400000000,0.346400000000,0.041700000000,0.293800000000,14460.122068965500,1205.010172413790),
(37.844913645631,0.350000000000,2.515916933154,0.711997109780,-0.131500000000,0.329900000000,-0.144400000000,0.014000000000,954.796551724138,79.566379310345)
)


#basics learned here:
#https://apmonitor.com/pdc/index.php/Main/NonlinearProgramming


################# Functions to describe Profit function. #########################################################

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

def profit_helper(aov,product_margin,intercept1,elasticity1,intercept2,elasticity2,cell1,cell3) :
    return make_profit(make_orders(make_clicks(intercept1,elasticity1),intercept2,elasticity2,cell1,cell3),aov,product_margin)

################# Functions to help with constraints. #####################################################
#Equality constraint means that the constraint function result is to be zero whereas inequality means that it is to be NON NEGATIVE
#Constraint Cheat Sheet (how to formulate your constraint function):
# A<=B  becomes B-A
# A=B   becomes B-A
# A>=B  becomes -(B-A)
#Alternately you can just specify the function and pass in limit values using scipy.optimize.NonLinearConstraint  (Way simpler)
#also: https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.NonlinearConstraint.html#scipy.optimize.NonlinearConstraint

#This is the easy way to describe a constraint function. Function only without limits.
#This function is simply summing up the specified spends.
def make_group_fn(start,end) :
    def group_fn(spends) :
        return sum(spends[start:end])
    return group_fn

#This is the alternate way of defining constraints.
#You bake the limit in to the equation, but it is not double ended constraint.
def make_group_fn_v2(start,end,limit) :
    def group_fn(spends) :
        return limit - sum(spends[start:end])
    return group_fn

#########################################################

def init_spends(ranges) :
    """
        Given a list of ranges (min,max) for each variable, init an array to a random value in the range.
        This array is the data structure that is used during calculation. the 'spends'
    :param ranges:
    :return: np array
    """
    #rand from 0-1
    rands = random.rand(1,len(ranges))[0]
    # min + (max-min)*rand
    return np.array(list(map(lambda x: x[0][0]+(x[0][1]-x[0][0])*x[1], zip(ranges,rands))))


#Objective function is sum of profits.
#Given a list of profit functions, and a list of spend variables (That we are optimizing)
#Also, we want to maximize (but python only provides minimize, so flip the sign)
def make_objective(profit_fns):
    def objective_fn(spends) :
        #         sum_eq = 0.0
        #         for i in range(0, len(profit_fns)):
        #             sum_eq = sum_eq + profit_fns[i](spends[i])
        #         return -sum_eq #flip the sign since we want to maximize
        return -sum(map(lambda x: x[0](x[1]), zip(profit_fns,spends)))
    return objective_fn

#Extract max,min from demo_data and transpose to min,max
spend_bounds = list(map(lambda x: (x[1],x[0]),map(lambda x: x[8:10], demo_data)))

#Generate the profit function for each item
profit_fns = list(map(lambda x: profit_helper(x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7]), demo_data))


################# CONSTRAINTS #########################################################
EPSILON = 0.01
#Sum of all spends. This constraint is unnecessary, and gnerally works better without it.
gall = NonlinearConstraint(make_group_fn(0,len(demo_data)), 0, 45000+(5*EPSILON))
#Sum of group spends
g1 = NonlinearConstraint(make_group_fn(0,10), 30097.0-EPSILON, 30097.0+EPSILON)
g2 = NonlinearConstraint(make_group_fn(10,16), 2358.0-EPSILON, 2358.0+EPSILON)
g3 = NonlinearConstraint(make_group_fn(16,23), 2578.0-EPSILON, 2578.0+EPSILON)
g4 = NonlinearConstraint(make_group_fn(23,30), 4734.0-EPSILON, 4734.0+EPSILON)
g5 = NonlinearConstraint(make_group_fn(30,37), 5233.0-EPSILON, 5233.0+EPSILON)
cons = ([g1,g2,g3,g4,g5,gall])

####Alternate way of defining constraints. I have seen it give totally wrong answers.
# gall = {'type': 'ineq', 'fun': make_group_fn_v2(0,len(demo_data),45000)}
# g1 = {'type': 'eq', 'fun': make_group_fn_v2(0,10,30097.0)}
# g2 = {'type': 'eq', 'fun': make_group_fn_v2(10,16,2358.0)}
# g3 = {'type': 'eq', 'fun': make_group_fn_v2(16,23,2578.0)}
# g4 = {'type': 'eq', 'fun': make_group_fn_v2(23,30,4734.0)}
# g5 = {'type': 'eq', 'fun': make_group_fn_v2(30,37,5233.0)}
# cons = ([gall,g1,g2,g3,g4,g5])


#####################################################################################

#Make the objective function.
objective = make_objective(profit_fns)


#Hacky way to retry several times.. Since the function is nonlinear, it may not converge.
#So we retry many times with different starting points.
retry=True
counter=0
solution=None
while retry and counter<100 :
    counter=counter+1
    try:
        spends = init_spends(spend_bounds)
        solution = minimize(objective,
                            spends,
                            method='SLSQP',
                            bounds=spend_bounds,
                            constraints=cons)
        print("success:" + str(counter))
        retry=False
    except:
        print("fail:" + str(counter))
        retry=True

#%%

print(solution.x)
print(sum(solution.x))
