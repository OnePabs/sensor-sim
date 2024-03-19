from common.Sim_math_ops import Sim_math_ops


class Distribution:
    def __init__(self, name="GENERAL", is_batch_size_independent=True):
        self.name = name
        self.is_batch_size_independent = is_batch_size_independent

    def create(self, data, write_to_file=False, filepath="", append=False):
        if write_to_file:
            Distribution.write_list_of_numbers(list_of_numbers=data, filepath=filepath, append=append)
            return data
        else:
            return data

    @staticmethod
    def write_list_of_numbers(list_of_numbers, filepath, append=False):
        #print("Parent Distribution write_list_of_numbers filepath = " + filepath)
        f = ''
        if append:
            f = open(filepath, "a")
            f.write("\n")
        else:
            f = open(filepath, "w")
        num_items = len(list_of_numbers)
        for i in range(num_items):
            f.write(str(list_of_numbers[i]))
            if i != num_items - 1:
                f.write("\n")
        f.close()
        return


class Constant(Distribution):
    def __init__(self, constant, is_batch_size_independent=True):
        super().__init__(name="CONSTANT", is_batch_size_independent=is_batch_size_independent)
        self.constant = constant

    def change_settings(self, constant):
        self.constant = constant
        return

    def create(self, n, write_to_file=False, filepath="", append=False):
        data = n*[self.constant]
        return super().create(data, write_to_file, filepath, append)


class ConstantRunningTotal(Distribution):
    def __init__(self, constant, start_point=0, is_batch_size_independent=True):
        super().__init__(name="CONSTANTRUNNING", is_batch_size_independent=is_batch_size_independent)
        self.constant = constant
        self.start_point = start_point

    def change_settings(self, constant, start_point=0):
        self.constant = constant
        self.start_point = start_point
        return

    def create(self, n, write_to_file=False, filepath="", append=False):
        data = n * [0]
        data[0] = self.start_point
        for i in range(1, n):
            data[i] = data[i-1] + self.constant
        return super().create(data, write_to_file, filepath, append)


class Exponential(Distribution):
    def __init__(self, mean, is_batch_size_independent=True):
        super().__init__(name="Exponential", is_batch_size_independent=is_batch_size_independent)
        self.mean = mean

    def change_settings(self, mean):
        self.mean = mean
        return

    def create(self, n, write_to_file=False, filepath="", append=False):
        data = n*[0]
        for i in range(n):
            data[i] = Sim_math_ops.exp(self.mean)
        return super().create(data, write_to_file, filepath, append)


class Poisson(Distribution):
    def __init__(self, mean, start_point=0, is_batch_size_independent=True):
        super().__init__(name="Poisson", is_batch_size_independent=is_batch_size_independent)
        self.mean = mean
        self.start_point = start_point
        return

    def change_settings(self, mean, start_point=0):
        self.mean = mean
        self.start_point = start_point
        return

    def create(self, n, write_to_file=False, filepath="", append=False):
        data = n * [0]
        if self.start_point > 0:
            data[0] = self.start_point + Sim_math_ops.exp(self.mean)
        for i in range(1, n):
            data[i] = data[i-1] + Sim_math_ops.exp(self.mean)
        return super().create(data, write_to_file, filepath, append)


class MultipleBarsConstant(Distribution):
    # __--__--__--__--
    def __init__(self, first_part_intervals, second_part_intervals, n_per_cycle, load_factor, is_batch_size_independent=True):
        # high: the value of the inter arrival times for the high bar
        # first_part_intervals: the value of the intervals for the first part until n_per_cycle*load_factor
        # second_part_ia: the value of the intervals for the second part from n_per_cycle*load_factor to n_per_cycle
        # nPerCycle: the number of points in one cycle. where one cycle is one repeating pattern of bars i.e __--
        # load_factor: the fraction of number of points at low value and all points in one cycle. = n_low/(n_low+n_high)
        super().__init__(name="MultipleBarsConstant", is_batch_size_independent=is_batch_size_independent)
        self.first_part_intervals = first_part_intervals
        self.second_part_intervals = second_part_intervals
        self.n_per_cycle = n_per_cycle
        self.load_factor = load_factor
        return

    def change_settings(self, first_part_intervals, second_part_intervals, n_per_cycle, load_factor):
        self.first_part_intervals = first_part_intervals
        self.second_part_intervals = second_part_intervals
        self.n_per_cycle = n_per_cycle
        self.load_factor = load_factor
        return

    def create(self, n, write_to_file=False, filepath="", append=False):
        # n is the number of points to create
        data = n * [0]
        for i in range(n):
            if i%self.n_per_cycle < self.load_factor*self.n_per_cycle:
                # use low value
                data[i] = self.first_part_intervals
            else:
                data[i] = self.second_part_intervals
        return super().create(data, write_to_file, filepath, append)


class MultipleBarsExponential(Distribution):
    def __init__(self, first_part_intervals, second_part_intervals, n_per_cycle, load_factor, is_batch_size_independent=True):
        # high: the value of the inter arrival times for the high bar
        # first_part_intervals: the value of the intervals for the first part until n_per_cycle*load_factor
        # second_part_ia: the value of the intervals for the second part from n_per_cycle*load_factor to n_per_cycle
        # nPerCycle: the number of points in one cycle. where one cycle is one repeating pattern of bars i.e __--
        # load_factor: the fraction of number of points at low value and all points in one cycle. = n_low/(n_low+n_high)
        super().__init__(name="MultipleBarsExponential", is_batch_size_independent=is_batch_size_independent)
        self.first_part_intervals = first_part_intervals
        self.second_part_intervals = second_part_intervals
        self.n_per_cycle = n_per_cycle
        self.load_factor = load_factor
        return

    def change_settings(self, first_part_intervals, second_part_intervals, n_per_cycle, load_factor):
        self.first_part_intervals = first_part_intervals
        self.second_part_intervals = second_part_intervals
        self.n_per_cycle = n_per_cycle
        self.load_factor = load_factor
        return

    def create(self, n, write_to_file=False, filepath="", append=False):
        # n is the number of points to create
        data = n * [0]
        comp = int(round(self.load_factor * self.n_per_cycle))
        for i in range(n):
            if i % self.n_per_cycle < comp:
                # use low value
                data[i] = Sim_math_ops.exp(self.first_part_intervals)
            else:
                data[i] = Sim_math_ops.exp(self.second_part_intervals)
        return super().create(data=data, write_to_file=write_to_file, filepath=filepath, append=append)



class MultipleBarsPoisson(Distribution):
    # __--__--__--__--
    def __init__(self, low_request_rate, high_request_rate, num_req_per_cycle, load_factor, is_batch_size_independent=True):
        # high: the value of the inter arrival times for the high bar
        # low_request_rate: The low request rate used
        # high_request_rate: high_request_rate used
        # req_per_cycle: number of requests per cycle
        # load_factor: the fraction of requests that have a low request rate
        # (i.e. load_factor = #req_with_low_rate/req_per_cycle
        super().__init__(name="MultipleBarsPoisson", is_batch_size_independent=is_batch_size_independent)
        self.low_request_rate = low_request_rate
        self.high_request_rate = high_request_rate
        self.num_req_per_cycle = num_req_per_cycle
        self.load_factor = load_factor
        self.num_req_with_low_rate_per_cycle = int(num_req_per_cycle*load_factor)
        self.num_req_with_high_rate_per_cycle = num_req_per_cycle - self.num_req_with_low_rate_per_cycle
        return

    def create(self, n, write_to_file=False, filepath="", append=False):
        # n is the number of points to create
        if n % self.num_req_per_cycle != 0:
            n = int(n/self.num_req_per_cycle)*self.num_req_per_cycle
        data = n*[0]
        for i in range(1, n):
            if i % self.num_req_per_cycle <= self.num_req_with_low_rate_per_cycle:
                # use low value
                data[i] = data[i-1] + Sim_math_ops.exp_rate(self.low_request_rate)
            else:
                data[i] = data[i-1] + Sim_math_ops.exp_rate(self.high_request_rate)
        return super().create(data=data, write_to_file=write_to_file, filepath=filepath, append=append)





### STORAGE CLOUD SERVICE TIME BATCH DEPENDENT
class ExponentialBatchSizeDependent(Distribution):
    def __init__(self, mean_access_time, mean_request_service_time, is_batch_size_independent=False):
        super().__init__(name="ExponentialBatchSizeDependent", is_batch_size_independent=is_batch_size_independent)
        self.mean_access_time = mean_access_time
        self.mean_request_service_time = mean_request_service_time
        self.access_time_distribution = Exponential(mean_access_time)
        self.request_service_time_distribution = Exponential(mean_request_service_time)
        return

    def create(self, n, write_to_file=False, filepath="", append=False):
        # n is the number of requests in the batch for which a service time is demanded
        # the final service time is divided into n equal service times for the n requests
        access_time = self.access_time_distribution.create(1)
        request_times = self.request_service_time_distribution.create(n)
        avg_st = float(sum(access_time) + sum(request_times))/n
        data = n*[avg_st]
        return super().create(data=data, write_to_file=write_to_file, filepath=filepath, append=append)


