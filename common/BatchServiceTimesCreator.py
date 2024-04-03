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


class Hard_disk_st:
    def __init__(self,
                 seek_time,         # in milliseconds
                 rpm,               # disk rotations per minute
                 transfer_rate,     # bytes per millisecond
                 block_size):       # bytes
        self.seek_time_creator = Exponential_st(seek_time)

        minutes_per_rotation = 1/rpm
        milliseconds_per_rotation = minutes_per_rotation*60*1000
        mean_rotation_time = milliseconds_per_rotation/2
        self.rotation_time_creator = Exponential_st(mean_rotation_time)

        self.block_size = block_size

        mean_block_write_time = block_size/transfer_rate
        self.block_write_time_creator = Exponential_st(mean_block_write_time)
        return

    def create_next(self, batch):
        # Rotational/Hard Drive service time =  Seek Time + Rotational Latency + Transfer Time
        seek_time = self.seek_time_creator.create_next(None)
        rotation_time = self.rotation_time_creator.create_next(None)

        transfer_time = 0
        num_blocks = math.ceil(batch.get_size()/self.block_size)
        for i in range(num_blocks):
            transfer_time += self.block_write_time_creator.create_next(None)

        return seek_time + rotation_time + transfer_time



# testing
n = 10000
device_service_time_creator = Hard_disk_st(seek_time=5, rpm=7200, transfer_rate=80000, block_size=4000)
sts = n*[0]

from common.Batch import Batch
batch = Batch()

from common.Request import Request
req = Request(arrival_time=0, size=1024)

batch.add_request_to_batch(req)

for i in range(n):
    sts[i] = device_service_time_creator.create_next(batch)

import statistics
mean = statistics.mean(sts)
print(mean)



