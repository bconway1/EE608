from sympy import *
import matplotlib.pyplot as plt
import math
#crude oil output, in millions of barrels per day
y1 = Symbol('y1')
#crude oil nominal price, in U.S. dollars per barrel;
y2 = Symbol('y2')
#Real GDP index
z = Symbol('z')
c = Symbol('c')
#crude oil demand price elasticity 1974 - 2004
delta = -0.003
#crude oil demand income elasticity 1974 - 2004
gamma = 1.49

demand = y1 + delta*y2 + gamma*z
#oil output cant be more than before oil storage crisis
#source: https://www.statista.com/statistics/271823/daily-global-crude-oil-demand-since-2006/
c1 = y1 - math.log(101000000, 10)
c2 = -y1 + math.log(90000000, 10)
#GDP cant be better than before crisis
#source: https://fred.stlouisfed.org/series/GDPC1
c3 = z - math.log(19221970000000, 10)
#

# g_pen_1 = g + c * (c1**2)
# g_pen_2 = g + c * (c2**2)
# g_pen_3 = g + c * (c3**2)
# g_pen_4 = g + c * (c4**2)

yk1 = 75000000
yk2 = 60
zk = 20221970000000

epsilon = 1/100
alpha = 0.001
c_value = 1
eta = 1.01
iterations = 0
first_few_iter = 50
max_iterations = 5000
j = 1
iter_for_plot = 20
iterations_first_few_list = list()
function_value_first_few_list = list()
while True:
    iterations =+ 1
    if N(c1.subs(y1, yk1)).evalf() > 0:
        c1_temp = c1
    else:
        c1_temp = 0
    if N(c2.subs(y1, yk1)).evalf() > 0:
        c2_temp = c2
    else:
        c2_temp = 0
    if N(c3.subs(z, zk)).evalf() > 0:
        c3_temp = c3
    else:
        c3_temp = 0


    theta = demand + c *( ((c1)**2) + ((c2)**2) + ((c3)**2) )
    theta_diff_y1 = theta.diff(y1)
    theta_diff_y2 = theta.diff(y2)
    theta_diff_z = theta.diff(z)

    yk1_plus_1 = yk1 - alpha * N(theta_diff_y1.subs(y1, math.log(yk1, 10)).subs(y2, math.log(yk2, 10)).subs(z, math.log(zk, 10)).subs(c, c_value)).evalf()
    yk2_plus_2 = yk2 - alpha * N(theta_diff_y2.subs(y2, math.log(yk2, 10)).subs(z, math.log(zk, 10)).subs(y1, math.log(yk1, 10)).subs(c, c_value)).evalf()
    zk_plus_1 = zk -alpha * N(theta_diff_z.subs(z, math.log(zk, 10)).subs(y2, math.log(yk2, 10)).subs(y1, math.log(yk1, 10)).subs(c, c_value)).evalf()

    if (abs(yk1_plus_1 - yk1) < epsilon) or (abs(yk2_plus_2 - yk2) < epsilon) or (abs(zk_plus_1 - zk) < epsilon):
        yk1 = yk1_plus_1
        yk2 = yk2_plus_2
        zk = zk_plus_1
        break
    if abs((N(demand.subs(y1, yk1).subs(y2, yk2).subs(z, zk)).evalf()) - (N(demand.subs(y1, yk1_plus_1).subs(y2, yk2_plus_2)).subs(z, zk_plus_1).evalf())) < epsilon :
        yk1 = yk1_plus_1
        yk2 = yk2_plus_2
        zk = zk_plus_1
        break

    yk1 = yk1_plus_1
    yk2 = yk2_plus_2
    zk = zk_plus_1
    c_value = c_value * eta

    if j < iter_for_plot:
        iterations_first_few_list.append(j)
        function_value_first_few_list.append(N(demand.subs(y1, yk1).subs(y2, yk2)).evalf())
        j += 1
    if iterations > max_iterations:
        break


print("minimizer is: y1 =  ", yk1, " and y2 = ", yk2, " and z = ", zk, "\n")
print("The min of the func is demandS = ", N(demand.subs(y1, yk1).subs(y2, yk2).subs(z, zk)).evalf())

plt.plot(iterations_first_few_list, function_value_first_few_list)
plt.ylabel('function value')
plt.xlabel('iteration number')
plt.show()