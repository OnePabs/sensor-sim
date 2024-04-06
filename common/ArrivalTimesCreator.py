from common.Sim_math_ops import Sim_math_ops


class Constant_inter_arrival_times:
    def __init__(self, inter_arrival_time):
        self.inter_arrival_time = inter_arrival_time

    def create(self, num_requests):
        arrival_times = num_requests * [0]
        for i in range(1, num_requests):
            arrival_times[i] = arrival_times[i - 1] + self.inter_arrival_time
        return arrival_times


class Exponential_inter_arrival_times:
    def __init__(self, mean_inter_arrival_time):
        self.mean_inter_arrival_time = mean_inter_arrival_time

    def create(self, num_requests):
        arrival_times = num_requests * [0]
        for i in range(1, num_requests):
            arrival_times[i] = arrival_times[i - 1] + Sim_math_ops.exp(self.mean_inter_arrival_time)
        return arrival_times


class Multiple_sources_exponential_inter_arrival_times:
    def __init__(self, mean_inter_arrival_times):
        self.mean_inter_arrival_times = mean_inter_arrival_times

    def create(self, num_requests):
        arrival_times = []
        for source_idx in range(len(self.mean_inter_arrival_times)):
            creator = Exponential_inter_arrival_times(self.mean_inter_arrival_times[source_idx])
            arrival_times.extend(creator.create(num_requests))
        arrival_times.sort()
        return arrival_times[:num_requests]



