from ml_models.Model import Model


class NoBufferingModel(Model):

    def __init__(self):
        super().__init__()
        self.display_name = "No Buffering"
        return

    def predict_next_inter_arrival(self, k_latest_inter_arrivals):
        return 0

    def predict_next_request_size(self, k_latest_request_sizes):
        return 0

    def predict_batch_service_time(self, batch_size):
        return 0

    def predict_multiple_batches_service_times(self, batch_sizes):
        return len(batch_sizes)*[0]





