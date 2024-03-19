from common.BatchHandler import *
from common.Sim_math_ops import *
import statistics

class Simulator:
    @staticmethod
    def simulate(arrival_time_distribution,
                 access_times_distribution,
                 write_times_distribution,
                 ia_predictor=0,
                 st_predictor=0,
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

                curr_num_batches = batch_handler.get_num_batches_in_server_queue(arrival_times[j])
                service_done = batch_handler.get_service_time_already_done_on_request_being_serviced(arrival_times[j])
                expected_service_time_per_batch = 40
                expected_inter_arrival_time = 50
                if expected_inter_arrival_time < (service_done + expected_service_time_per_batch*curr_num_batches):
                    # Buffer (Do not send request and buffer contents to the server)
                    send_buffer_contents_to_server = False
                else:
                    # Transmit (send request and buffer contents to the server)
                    send_buffer_contents_to_server = True

                if send_buffer_contents_to_server:
                    batch_handler.send_current_batch_to_service()

            e = batch_handler.calculate_avg_E()
            #print(e)
            Es.append(e)


        # experiments finished
        z_or_t_score = Sim_math_ops.get_z_or_t_score(confidence_level=0.95, number_of_samples=num_experiments)

        avg_E = statistics.mean(Es)
        E_std = statistics.stdev(Es, xbar=avg_E)
        ME = z_or_t_score * (E_std / math.sqrt(num_experiments))

        print('Average E: ' + str(avg_E))
        print('ME: ' + str(ME))

        return avg_E, ME

