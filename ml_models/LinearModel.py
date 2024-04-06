from ml_models.Model import Model
from common.ArrivalTimesCreator import Exponential_inter_arrival_times
from common.RequestSizeCreator import Exponential_request_sizes
from sklearn import linear_model
import pandas as pd
import numpy as np
import math


class LinearModel(Model):

    def __init__(self):
        super().__init__()
        self.display_name = "Linear Regression"
        return

    def train_inter_arrival_predictor(self, k):
        # create data
        num_samples_per_mean_ia = 1000
        num_ia_per_sample = 50
        mean_rates = [1, 5, 10, 15, 20]
        mean_ias = [1000/x for x in mean_rates]

        # create data
        inputs = []
        labels = []
        for mean_ia in mean_ias:
            arrival_times_creator = Exponential_inter_arrival_times(mean_ia)
            for sample_idx in range(num_samples_per_mean_ia):
                inputs.append(arrival_times_creator.create(num_ia_per_sample))
                labels.append(mean_ia)

        # convert data to pandas dataframe
        inputs = pd.DataFrame(inputs)
        labels = pd.DataFrame(labels)

        # create model
        self.ia_predictor = linear_model.LinearRegression()

        # fit the model
        self.ia_predictor.fit(inputs, labels)
        return

    def train_request_size_predictor(self, k):
        # create data
        num_samples_per_mean_req_size = 1000
        num_req_per_sample = 50
        mean_req_sizes = [100, 1000, 10000, 100000]

        # create data
        inputs = []
        labels = []
        for mean_req_size in mean_req_sizes:
            request_sizes_creator = Exponential_request_sizes(mean_req_size)
            for sample_idx in range(num_samples_per_mean_req_size):
                inputs.append(request_sizes_creator.create(num_req_per_sample))
                labels.append(mean_req_size)

        # convert data to pandas dataframe
        inputs = pd.DataFrame(inputs)
        labels = pd.DataFrame(labels)

        # create model
        self.req_size_predictor = linear_model.LinearRegression()

        # fit the model
        self.req_size_predictor.fit(inputs, labels)
        return

    def train_service_time_predictor(self,
                                     access_time,       # in milliseconds
                                     transfer_rate,     # bytes per millisecond
                                     block_size         # bytes
                                     ):
        # create data
        block_write_time = block_size/transfer_rate
        data_size = list(range(1000000))
        expected_storage_times = [access_time + math.ceil(x/block_size)*block_write_time for x in data_size]

        # convert data to pandas dataframe
        inputs = pd.DataFrame(data_size)
        labels = pd.DataFrame(expected_storage_times)

        # create model
        self.st_predictor = linear_model.LinearRegression()

        # fit the model
        self.st_predictor.fit(inputs, labels)
        return





