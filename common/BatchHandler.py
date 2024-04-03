from common.Batch import Batch


class BatchHandler:
    def __init__(self, num_requests):
        # either enter the distribution or enter the service times
        self.num_requests = num_requests
        self.batches = []
        self.current_batch = Batch()

    def add_request_to_current_batch(self, request):
        self.current_batch.add_request_to_batch(request)
        return

    def send_current_batch_to_service(self, network_delay, processing_time):
        batch = self.current_batch

        # set buffer exit time
        batch.set_buffer_exit_time()

        # set network_delay
        batch.set_network_delay(network_delay)

        # set server entry time
        batch.set_server_entry_time()

        # calculate batch  service time start (the start of the processing time)
        if len(self.batches) == 0 or batch.server_entry_time >= self.batches[-1].system_exit_time:
            batch.start_service_time = batch.server_entry_time
        else:
            batch.start_service_time = self.batches[-1].system_exit_time

        # set batch service time
        batch.service_time = processing_time

        # set system exit time
        batch.set_system_exit_time()

        # set requests end-to-end times
        batch.set_end_to_end_times()

        # append to list of batches that have fields already calculated
        self.batches.append(self.current_batch)

        # create a new current batch
        self.current_batch = Batch()

        return



