import numpy as np
class Model:
    def __init__(self):
        self.display_name = "Model"
        self.ia_predictor = None
        self.req_size_predictor = None
        self.st_predictor = None
        return

    def get_display_name(self):
        return self.display_name

    def train_inter_arrival_predictor(self, k):
        return

    def train_request_size_predictor(self, k):
        return

    def train_service_time_predictor(self, access_time, transfer_rate, block_size):
        return

    def train(self, k, access_time, transfer_rate, block_size):
        self.train_inter_arrival_predictor(k)
        self.train_request_size_predictor(k)
        self.train_service_time_predictor(access_time, transfer_rate, block_size)
        return

    def predict_next_inter_arrival(self, k_latest_inter_arrivals):
        return self.ia_predictor.predict([k_latest_inter_arrivals])[0][0]

    def predict_next_request_size(self, k_latest_request_sizes):
        return self.req_size_predictor.predict([k_latest_request_sizes])[0][0]

    def predict_batch_service_time(self, batch_size):
        return self.st_predictor.predict([[batch_size]])[0]

    def predict_multiple_batches_service_times(self, batch_sizes):
        return self.st_predictor.predict(batch_sizes)



