from common.Sim_math_ops import Sim_math_ops
import math


class Constant_st:
    def __init__(self, constant):
        self.constant = constant

    def create_next(self, batch):
        return self.constant


class Exponential_st:
    def __init__(self, mean):
        self.mean = mean

    def create_next(self, batch):
        return Sim_math_ops.exp(self.mean)


class Hard_disk:
    def __init__(self, mean_access_time, mean_block_write_time, block_size):
        self.mean_access_time = mean_access_time
        self.mean_block_write_time = mean_block_write_time
        self.block_size = block_size

    def create_next(self, batch):
        num_bocks = math.ceil(batch.get_size())
        return Sim_math_ops.exp(self.mean)





