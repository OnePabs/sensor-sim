from common.Sim_math_ops import Sim_math_ops


class Constant_request_sizes:
    def __init__(self, request_size):
        self.request_size = request_size

    def create(self, num_requests):
        return num_requests * [self.request_size]


class Exponential_request_sizes:
    def __init__(self, mean_request_size):
        self.mean_request_size = mean_request_size

    def create(self, num_requests):
        sizes = num_requests*[0]
        for i in range(num_requests):
            sizes[i] = Sim_math_ops.exp(self.mean_request_size)
        return sizes

