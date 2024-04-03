
class test_st_constant_predictor:
    def __init__(self, constant):
        self.constant = constant

    def predict(self, batch_sizes):
        num_predictions = len(batch_sizes)
        predictions = num_predictions*[0]
        for i in range(num_predictions):
            predictions[i] = self.constant
        return predictions
