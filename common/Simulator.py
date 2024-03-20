import pandas as pd

from common.BatchHandler import *
from common.Sim_math_ops import *
import statistics

class Simulator:
    @staticmethod
    def simulate(arrival_time_distribution,
                 access_times_distribution,
                 write_times_distribution,
                 ia_predictor,
                 st_predictor,
                 num_ia_per_input=50,
                 num_batches_per_input=50,
                 num_requests=10000,
                 num_experiments=30):
        Es = []

        for exp_num in range(num_experiments):
            arrival_times = arrival_time_distribution.create(num_requests)
            access_times = access_times_distribution.create(num_requests)
            write_times = write_times_distribution.create(num_requests)

            batch_handler = BatchHandler(num_requests)
            for j in range(num_requests):
                batch_handler.add_request_to_current_batch(arrival_times[j],
                                                           access_times[j],
                                                           write_times[j])

                if j > num_ia_per_input and len(batch_handler.batches) >= num_batches_per_input:
                    # there is enough data to make a prediction on wheter to buffer or not

                    curr_num_batches_in_server_queue = batch_handler.get_num_batches_in_server_queue(arrival_times[j])
                    service_done = batch_handler.get_service_time_already_done_on_request_being_serviced(arrival_times[j])

                    ia_inputs = [Sim_math_ops.get_inter_arrival_times(arrival_times[j-50:j+1])]
                    st_inputs = [batch_handler.get_latest_batch_service_times(num_batches_per_input)]

                    expected_inter_arrival_time = ia_predictor.predict(ia_inputs)[0]
                    expected_service_time_per_batch = st_predictor.predict(st_inputs)[0]

                    if service_done == -1:
                        # no batch being serviced
                        service_time_remaining = 0
                    else:
                        service_time_remaining = expected_service_time_per_batch - service_done

                    if expected_inter_arrival_time <= (service_time_remaining + expected_service_time_per_batch*curr_num_batches_in_server_queue):
                        # Buffer (Do not send request and buffer contents to the server)
                        send_buffer_contents_to_server = False
                    else:
                        # Transmit (send request and buffer contents to the server)
                        send_buffer_contents_to_server = True
                else:
                    send_buffer_contents_to_server = True

                if send_buffer_contents_to_server:
                    batch_handler.send_current_batch_to_service()

            #print(batch_handler.batches)
            e = batch_handler.calculate_avg_E()
            Es.append(e)


        # experiments finished
        z_or_t_score = Sim_math_ops.get_z_or_t_score(confidence_level=0.95, number_of_samples=num_experiments)

        avg_E = statistics.mean(Es)
        E_std = statistics.stdev(Es, xbar=avg_E)
        ME = z_or_t_score * (E_std / math.sqrt(num_experiments))

        return avg_E, ME

