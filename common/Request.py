

class Request:
    def __init__(self, arrival_time, size):
        self.arrival_time = arrival_time
        self.size = size
        self.end_to_end_time = -1

    def get_arrival_time(self):
        return self.arrival_time

    def get_size(self):
        return self.size

    def set_end_to_end_time(self, system_exit_time):
        self.end_to_end_time = system_exit_time - self.arrival_time

    def get_end_to_end_time(self):
        return self.end_to_end_time





