import numpy as np  # linear algebra
import math
import statistics
import scipy

class Sim_math_ops:

    @staticmethod
    def get_z_or_t_score(confidence_level, number_of_samples):
        upper_tail_quantile = confidence_level + (1 - confidence_level)/2
        if number_of_samples < 30:
            # use student t distribution
            df = number_of_samples - 1  # degrees of freedom
            return scipy.stats.t.ppf(upper_tail_quantile, df)
        else:
            # use normal distribution
            return scipy.stats.norm.ppf(upper_tail_quantile)

    @staticmethod
    def binary_txt_to_int(b):
        # removes last binary digit of b
        sum = 0
        reverse_idx = -2
        for i in range(len(b)-1):
            sum = sum + pow(2, i) * int(b[reverse_idx])
            reverse_idx = reverse_idx - 1
        return sum

    @staticmethod
    def create_experiment_return_object(arrival_times, batches):
        # calculate performance metrics
        measured_avg_inter_arrival_time = Sim_math_ops.avg_inter_arrival(arrival_times)
        buffer_mean_residence_time = Sim_math_ops.get_average_buffer_residence_time(batches)
        storage_cloud_mean_batch_inter_arrival_time = Sim_math_ops.get_storage_cloud_mean_batch_inter_arrival_time(batches)
        storage_cloud_mean_service_time = Sim_math_ops.get_mean_batch_service_time(batches)
        storage_cloud_mean_residence_time = Sim_math_ops.get_average_metric_from_batches(batches, "storage_cloud_residence_time")
        mean_end_to_end_time = Sim_math_ops.get_average_end_to_end_time(batches)
        return_object = {
            'buffer_mean_inter_arrival_time': measured_avg_inter_arrival_time,
            'buffer_mean_residence_time': buffer_mean_residence_time,
            'storage_cloud_mean_batch_inter_arrival_time': storage_cloud_mean_batch_inter_arrival_time,
            'storage_cloud_mean_service_time': storage_cloud_mean_service_time,
            'storage_cloud_mean_residence_time': storage_cloud_mean_residence_time,
            'E': mean_end_to_end_time
        }
        return return_object




    ###################################
    ### FUNCTIONS FOR DISTRIBUTIONS ###
    ###################################
    @staticmethod
    def const(value):
        return value

    # this function generates numbers that are exponentialy distributed with a mean "mean"
    # It was taken from this website: https://www.weibull.com/hotwire/issue201/hottopics201.htm
    @staticmethod
    def exp(mean):
        return (-mean * math.log(1 - np.random.uniform(0, 1)))

    # this function generates numbers that are exponentialy distributed with a rate "rate"
    @staticmethod
    def exp_rate(rate):
        mean = 1000/rate
        return Sim_math_ops.exp(mean)






    ###################################
    #### LIST STATISTICS FUNCTIONS ####
    ###################################
    # this function calculates the average of numbers inside a list
    @staticmethod
    def average(lst):
        return sum(lst) / len(lst)

    @staticmethod
    def avg_inter_arrival(lst):
        lst2 = (len(lst) - 1) * [0]
        for i in range(1, len(lst)):
            lst2[i - 1] = lst[i] - lst[i - 1]
        return Sim_math_ops.average(lst2)

    @staticmethod
    def get_inter_arrival_times(arrival_times):
        arrival_times_len = len(arrival_times)
        if arrival_times_len < 2:
            print("ERROR: less than 2 items. cannot compute inter arrival times")
            exit()
        inter_arrival_times = (len(arrival_times)-1)*[0]
        for i in range(1, arrival_times_len):
            inter_arrival_times[i-1] = arrival_times[i] - arrival_times[i-1]
        return inter_arrival_times

    @staticmethod
    def get_arrival_times(inter_arrival_times):
        arrival_times = [0]*(len(inter_arrival_times)+1)
        for i in range(1, len(arrival_times)):
            arrival_times[i] = arrival_times[i-1] + inter_arrival_times[i-1]
        return arrival_times



    ################################
    ## BATCH STATISTICS FUNCTIONS ##
    ################################


    @staticmethod
    def get_average_metric_from_batches(batches, metric):
        sum = 0
        num = 0
        for curr_batch in batches:
            num += len(curr_batch["requests"])
            sum += len(curr_batch["requests"]) * curr_batch[metric]
        return sum/num

    @staticmethod
    def get_average_buffer_residence_time(batches):
        sum = 0
        num = 0
        for curr_batch in batches:
            sum += math.fsum(curr_batch["buffer_residence_times"])
            num += len(curr_batch["buffer_residence_times"])
        return sum/num

    @staticmethod
    def get_average_end_to_end_time(batches):
        sum = 0
        num = 0
        for curr_batch in batches:
            sum += math.fsum(curr_batch["end_to_end_times"])
            num += len(curr_batch["end_to_end_times"])
        return sum / num

    @staticmethod
    def get_mean_batch_service_time(batches):
        sum = 0
        num_batches = len(batches)
        for curr_batch in batches:
            sum += curr_batch["storage_cloud_service_time"]
        return sum/num_batches

    @staticmethod
    def get_storage_cloud_batch_throughput(batches):
        start = batches[0]["storage_cloud_service_time_start"]
        end = batches[-1]["storage_cloud_exit_time"]
        num_batches = len(batches)
        throughput = num_batches/(end - start)
        return throughput

    @staticmethod
    def get_storage_cloud_utilization(batches):
        throughput = Sim_math_ops.get_storage_cloud_batch_throughput(batches)
        #print("throughput: " + str(throughput*1000))
        mean_service_time = Sim_math_ops.get_mean_batch_service_time(batches)
        #print("mean_service_time: " + str(mean_service_time))
        u = throughput*mean_service_time
        #print("Utilization: " + str(u))
        #print()
        return u

    @staticmethod
    def get_storage_cloud_mean_batch_inter_arrival_time(batches):
        #print('length of batches = ' + str(len(batches)))
        list_of_batches_storage_cloud_arrival_times = len(batches)*[0]
        for idx in range(len(batches)):
            #print('batch storage cloud entry time: ' + str(batches[idx]["storage_cloud_entry_time"]))
            list_of_batches_storage_cloud_arrival_times[idx] = batches[idx]["storage_cloud_entry_time"]
        return Sim_math_ops.avg_inter_arrival(list_of_batches_storage_cloud_arrival_times)



