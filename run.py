from common.Simulator import Simulator
from common.Distributions import *

arrival_time_distribution = Poisson(50)
access_times_distribution = Exponential(40)
write_times_distribution = Constant(0)

avg_E, ME = Simulator.simulate(arrival_time_distribution,
                               access_times_distribution,
                               write_times_distribution)

print(avg_E)
print(ME)


