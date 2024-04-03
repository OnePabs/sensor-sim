from common.BatchHandler import *
from common.Sim_math_ops import *
from common.Request import Request
import statistics
from common.ArrivalTimesCreator import *
from common.RequestSizeCreator import *
from common.BatchServiceTimesCreator import *
from ml_models.test_st_constant_predictor import test_st_constant_predictor
from ml_models.test_req_size_constant_predictor import test_req_size_constant_predictor
from ml_models.test_ia_constant_predictor import test_ia_constant_predictor

class Simulator:
    @staticmethod
    def simulate(arrival_times_creator,
                 request_size_creator,
                 network_delay_creator,
                 batch_service_time_creator,
                 ia_predictor=None,
                 st_predictor=None,
                 req_size_predictor=None,
                 k=50,  # number of samples for prediction
                 num_requests=100000,
                 num_experiments=30):
        Es = []

        for exp_num in range(num_experiments):
            num_requests = 7
            arrival_times = [0, 10, 20, 30, 40, 50, 140] #arrival_times_creator.create(num_requests)
            request_sizes = [1, 2, 3, 4, 5, 6, 7] # request_size_creator.create(num_requests)
            requests = []
            for req_idx in range(num_requests):
                requests.append(Request(arrival_times[req_idx],
                                        request_sizes[req_idx]))

            batch_handler = BatchHandler(num_requests)
            for j in range(num_requests):
                batch_handler.add_request_to_current_batch(requests[j])

                if ia_predictor is None and st_predictor is None:
                    # perform no Buffering
                    send_buffer_contents_to_server = True
                elif j >= k or True:
                    # there is enough data to make a prediction on whether to buffer or not

                    # Find S_NB (service time for not buffering = S(sum(b(i) for i=1 to n))
                    current_batch_size = batch_handler.current_batch.get_size()
                    S_NB = st_predictor.predict([current_batch_size])[0]
                    print("S_NB: " + str(S_NB))

                    # Find S_B (service time for buffering = S(sum(b(i) for i=1 to n+1))
                    last_k_requests = request_sizes[j-k:j+1]
                    estimated_size_of_nex_request = req_size_predictor.predict(last_k_requests)[0]
                    estimated_buffering_batch_size = current_batch_size + estimated_size_of_nex_request
                    S_B = st_predictor.predict([estimated_buffering_batch_size])[0]
                    print("S_B: " + str(S_B))

                    # Find Q
                    Q = 0
                    current_time = requests[j].get_arrival_time()
                    if j>=1 and batch_handler.batches[-1].get_system_exit_time() > current_time:
                        batch_being_serviced_rev_idx = -1
                        is_batch_currently_being_serviced_reached = False
                        while not is_batch_currently_being_serviced_reached:
                            batch_start_service_time = batch_handler.batches[batch_being_serviced_rev_idx].get_start_service_time()
                            batch_system_exit_time = batch_handler.batches[batch_being_serviced_rev_idx].get_system_exit_time()
                            if batch_start_service_time <= current_time < batch_system_exit_time:
                                is_batch_currently_being_serviced_reached = True
                            else:
                                batch_being_serviced_rev_idx = batch_being_serviced_rev_idx - 1
                        # get the expected service times for the batches currently queued and the batch being serviced
                        sizes = []
                        batch_rev_idx = -1
                        while batch_rev_idx >= batch_being_serviced_rev_idx:
                            sizes.append(batch_handler.batches[batch_rev_idx].get_size())
                            batch_rev_idx = batch_rev_idx - 1
                        queue_service_times = st_predictor.predict(sizes)
                        service_already_done = current_time - batch_handler.batches[batch_being_serviced_rev_idx].get_start_service_time()
                        Q = sum(queue_service_times) - service_already_done
                    print("Q: " + str(Q))

                    # Find a
                    ia_inputs = [] #[Sim_math_ops.get_inter_arrival_times(arrival_times[j - num_ia_per_input:j + 1])]
                    a = ia_predictor.predict(ia_inputs)[0]
                    print("a: " + str(a))

                    # Find LHS (S_B - S_NB - min(Q,a))
                    lhs = S_B - S_NB - min(Q, a)
                    print("LHS: " + str(lhs))

                    # Find n
                    n = len(batch_handler.current_batch.requests)
                    print("n: " + str(n))

                    # Find Sum Ri
                    sum_ri = 0
                    last_req_arrival = batch_handler.current_batch.requests[-1].get_arrival_time()
                    for req in batch_handler.current_batch.requests:
                        sum_ri = sum_ri + (last_req_arrival - req.get_arrival_time())
                    print("sum_ri: " + str(sum_ri))

                    # Find Right Hand Side RHS = (1/(n^2 + n))*(sumRi - (n^2)*a)
                    rhs = (1/(pow(n, 2)+n))*(sum_ri - pow(n, 2)*a)
                    print("RHS: " + str(rhs))

                    # Find truth of inequality
                    ineq = lhs < rhs
                    print("ineq: " + str(ineq))

                    # determine if buffer should be sent
                    send_buffer_contents_to_server = not ineq
                    print("send_buff: " + str(send_buffer_contents_to_server))
                    print()

                    send_buffer_contents_to_server = True
                else:
                    send_buffer_contents_to_server = True

                if send_buffer_contents_to_server:
                    batch_handler.send_current_batch_to_service(
                        network_delay=network_delay_creator.create_next(batch_handler.current_batch),
                        processing_time=batch_service_time_creator.create_next(batch_handler.current_batch))

            # calculate end-to-end time
            e = 0
            for req in requests:
                e = e + req.get_end_to_end_time()
            e = e/num_requests
            Es.append(e)

        # experiments finished
        # z_or_t_score = Sim_math_ops.get_z_or_t_score(confidence_level=0.95, number_of_samples=num_experiments)
        #
        # avg_E = statistics.mean(Es)
        # E_std = statistics.stdev(Es, xbar=avg_E)
        # ME = z_or_t_score * (E_std / math.sqrt(num_experiments))
        #
        # return avg_E, ME



# sample run
arrival_times_creator = Exponential_inter_arrival_times(50)
request_size_creator = Exponential_request_sizes(100)
network_delay_creator = Constant_st(0)
batch_service_time_creator = Constant_st(40) #Exponential_st(40)
st_pred = test_st_constant_predictor(40)
req_size_predictor = test_req_size_constant_predictor(1)
ia_predictor = test_ia_constant_predictor(50)
#avg_E, ME =
Simulator.simulate(
    arrival_times_creator=arrival_times_creator,
    request_size_creator=request_size_creator,
    network_delay_creator=network_delay_creator,
    batch_service_time_creator=batch_service_time_creator,
    ia_predictor=ia_predictor,
    st_predictor=st_pred,
    req_size_predictor=req_size_predictor,
    num_experiments=1
)


#print("avg_E: " + str(avg_E) + ", ME: " + str(ME))
