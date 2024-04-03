
class test_req_size_constant_predictor:
    def __init__(self, constant):
        self.constant = constant

    def predict(self, last_k_requests):
        return [self.constant]