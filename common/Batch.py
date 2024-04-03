
class Batch:
    def __init__(self):
        self.requests = []
        self.size = 0
        self.buffer_exit_time = -1
        self.network_delay = -1
        self.server_entry_time = -1
        self.start_service_time = -1
        self.service_time = -1
        self.system_exit_time = -1

    def add_request_to_batch(self, request):
        self.requests.append(request)
        self.size = self.size + request.get_size()

    def get_size(self):
        return self.size

    def set_buffer_exit_time(self):
        self.buffer_exit_time = self.requests[-1].get_arrival_time()

    def set_network_delay(self, network_delay):
        self.network_delay = network_delay

    def set_server_entry_time(self):
        self.server_entry_time = self.buffer_exit_time + self.network_delay

    def set_start_service_time(self, start_service_time):
        self.start_service_time = start_service_time

    def get_start_service_time(self):
        return self.start_service_time

    def get_start_service_time(self):
        return self.start_service_time

    def set_service_time(self, service_time):
        self.service_time = service_time

    def set_system_exit_time(self):
        self.system_exit_time = self.start_service_time + self.service_time

    def get_system_exit_time(self):
        return self.system_exit_time

    def set_end_to_end_times(self):
        for req in self.requests:
            req.set_end_to_end_time(self.system_exit_time)


