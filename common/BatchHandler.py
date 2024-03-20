from common.Distributions import *

class BatchHandler:
    def __init__(self, num_requests):
        # either enter the distribution or enter the service times
        self.num_requests = num_requests
        self.batches = []
        self.create_new_current_batch()

    def create_new_current_batch(self):
        self.current_batch = {
            "batch_num": len(self.batches),
            "num_requests_in_batch": 0,
            "requests_arrival_times": [],
            "buffer_exit_time": 0,
            "start_service_time": 0,
            "access_times": [],
            "write_times": [],
            "total_service_time": 0,
            "system_exit_time": 0,
            "end_to_end_times": []
        }
        return


    def add_request_to_current_batch(self, system_arrival_time, access_time, write_time):
        self.current_batch["requests_arrival_times"].append(system_arrival_time)
        self.current_batch["access_times"].append(access_time)
        self.current_batch["write_times"].append(write_time)
        return


    def send_current_batch_to_service(self):
        self.current_batch["buffer_exit_time"] = self.current_batch["requests_arrival_times"][-1]
        self.current_batch["num_requests_in_batch"] = len(self.current_batch["requests_arrival_times"])

        # calculate batch  service time start
        if len(self.batches) == 0 or self.current_batch["buffer_exit_time"] >= self.batches[-1]["system_exit_time"]:
            self.current_batch["start_service_time"] = self.current_batch["buffer_exit_time"]
        else:
            self.current_batch["start_service_time"] = self.batches[-1]["system_exit_time"]

        # set batch service time
        st = self.current_batch["access_times"][0] + sum(self.current_batch["write_times"])
        self.current_batch["total_service_time"] = st

        #set batch exit time
        self.current_batch["system_exit_time"] = self.current_batch["start_service_time"] + self.current_batch["total_service_time"]

        # calc end_to_end_times
        for i in range(self.current_batch["num_requests_in_batch"]):
            e = self.current_batch["system_exit_time"] - self.current_batch["requests_arrival_times"][i]
            self.current_batch["end_to_end_times"].append(e)

        # add batch to list of batches
        self.batches.append(self.current_batch)

        # create a new current batch
        self.create_new_current_batch()

        return


    def calculate_avg_E(self):
        sum_E = 0
        for batch in self.batches:
            sum_E = sum_E + sum(batch["end_to_end_times"])
        return float(sum_E)/self.num_requests



    def get_num_batches_in_server_queue(self, current_time):
        if len(self.batches) == 0:
            #print("First batch")
            return 0
        last_idx = len(self.batches) - 1
        num_batches = 0
        curr_batch = self.batches[last_idx]
        while(curr_batch['start_service_time'] > current_time):
            num_batches = num_batches + 1
            last_idx = last_idx - 1
            curr_batch = self.batches[last_idx]
        return num_batches


    def get_service_time_already_done_on_request_being_serviced(self, current_time):
        # Returns:
        # -1 if there is no batch being serviced at the moment
        # n where n > 0 if there is a batch being serviced at the moment
        if len(self.batches) == 0:
            #print("First batch")
            return -1

        last_idx = len(self.batches) - 1
        last_batch = self.batches[last_idx]
        if last_batch['system_exit_time'] <= current_time:
            return -1
        else:
            # get to the batch that is being serviced
            curr_batch_idx = last_idx
            curr_batch = self.batches[curr_batch_idx]
            while curr_batch['start_service_time'] > current_time:
                curr_batch_idx = curr_batch_idx - 1
                curr_batch = self.batches[curr_batch_idx]

            # curr_batch now contains the batch being serviced
            return current_time - curr_batch['start_service_time']

    def get_latest_batch_service_times(self, num_batches_to_consider):
        if len(self.batches) < num_batches_to_consider:
            return -1

        batches_to_consider = self.batches[len(self.batches) - num_batches_to_consider:]
        batch_service_times = []
        for batch in batches_to_consider:
            batch_service_times.append(batch['total_service_time'])
        return batch_service_times
