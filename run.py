from common.Simulator import Simulator
from common.Distributions import *
import pickle

num_requests = 10000
num_experiments = 10

mean_ia = 50
mean_st = 28.57

num_ia_per_input = 50
num_batches_per_input = 50

arrival_time_distribution = Poisson(mean_ia)
access_times_distribution = Exponential(mean_st)
write_times_distribution = Constant(0)

linear_ia_predictor_path = 'ml_models/compressed_models/linear_ia_predictor.pkl'
with open(linear_ia_predictor_path, 'rb') as f:
    ia_predictor = pickle.load(f)

linear_st_predictor_path = 'ml_models/compressed_models/linear_st_predictor.pkl'
with open(linear_st_predictor_path, 'rb') as f:
    st_predictor = pickle.load(f)


avg_E, ME = Simulator.simulate(arrival_time_distribution=arrival_time_distribution,
                               access_times_distribution=access_times_distribution,
                               write_times_distribution=write_times_distribution,
                               ia_predictor=ia_predictor,
                               st_predictor=st_predictor,
                               num_ia_per_input=num_ia_per_input,
                               num_batches_per_input=num_batches_per_input,
                               num_requests=num_requests,
                               num_experiments=num_experiments)

print('Average E: ' + str(avg_E))
print('ME: ' + str(ME))


