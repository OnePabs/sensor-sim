from common.Simulator import Simulator
from common.ArrivalTimesCreator import *
from common.RequestSizeCreator import *
from common.BatchServiceTimesCreator import *
from ml_models.NoBufferingModel import NoBufferingModel
from ml_models.LinearModel import LinearModel
import pandas as pd


# Experiment Variables
verbose = True
results_folder_path = "results"
num_req_per_experiment = 10000
num_repetitions = 30
perform_ia_experiments=True
perform_nt_experiments=True
perform_at_experiments=True
perform_tr_experiments=True
perform_bs_experiments=True
perform_num_sources_experiments=True
default_mean_ia = 1000/10
default_mean_request_size = 5 #1000
default_mean_nt = 0 #1000/15
default_mean_at = 40
default_transfer_rate = 80000
default_block_size = 4000
default_k = 50
default_arrival_times_creator = Exponential_inter_arrival_times(default_mean_ia)
default_request_size_creator = Exponential_request_sizes(default_mean_request_size)
default_network_delay_creator = Exponential_st(default_mean_nt)
default_device_service_time_creator = Storage_with_access_time_and_blocks_st(access_time=default_mean_at,
                                                                             transfer_rate=default_transfer_rate,
                                                                             block_size=default_block_size)
no_buffering_model = NoBufferingModel()
linear_model = LinearModel()
models = [linear_model] #[no_buffering_model, linear_model]

# train models to default values
for model in models:
    model.train(k=default_k,
                access_time=default_mean_at,
                transfer_rate=default_transfer_rate,
                block_size=default_block_size)


print("default Inter Arrival Time: " + str(default_mean_ia))
print("default network delay: " + str(default_mean_nt))
print("default Access time: " + str(default_mean_at))
print("default Transfer Rate (bytes per millisecond): " + str(default_transfer_rate))
print("default Block Size (bytes): " + str(default_mean_at))

#######################
#### IA experiments ###
#######################
arrival_rates = [20] #[1, 5, 10, 15, 20]
mean_ias = [1000/x for x in arrival_rates]
if perform_ia_experiments:
    print("IA experiments")

    # write column headers
    filepath = results_folder_path + "/ia-experiments.txt"
    f = open(filepath, "w")
    f.write("Arrival Rate")
    for model in models:
        f.write("," + model.get_display_name() + ", ME")
    f.close()

    # perform experiments
    for mean_ia_idx in range(len(mean_ias)):
        mean_ia = mean_ias[mean_ia_idx]
        print("ia=" + str(mean_ia))
        f = open(filepath, "a")
        f.write("\n")
        f.write(str(mean_ia))
        f.close()
        arrival_time_creator = Exponential_inter_arrival_times(mean_ia)
        for model in models:
            avg_E, ME = Simulator.simulate(
                arrival_times_creator=arrival_time_creator,
                request_size_creator=default_request_size_creator,
                network_delay_creator=default_network_delay_creator,
                batch_service_time_creator=default_device_service_time_creator,
                model=model,
                k=50,
                num_requests=num_req_per_experiment,
                num_experiments=num_repetitions
            )

            if verbose:
                print(model.get_display_name() + " avg_E: " + str(avg_E) + ", ME: " + str(ME))
            # write data to file
            f = open(filepath, "a")
            f.write("," + str(avg_E) + "," + str(ME))
            f.close()



        #
        #
        # #################################
        # ### Network delay experiments ###
        # #################################
        # mean_nts = [0, 2, 4, 6, 8, 10]
        # if self.perform_nt_experiments:
        #     rows = []
        #     for mean_nt in mean_nts:
        #         print("NT experiment: nt=" + str(mean_nt))
        #         network_delay_creator = Exponential_st(mean_nt)
        #         avg_E, ME = Simulator.simulate(
        #             arrival_times_creator=default_arrival_times_creator,
        #             network_delay_creator=network_delay_creator,
        #             batch_service_time_creator=default_device_service_time_creator,
        #             ia_predictor=self.ia_predictor,
        #             st_predictor=self.st_predictor,
        #             req_size_predictor=self.req_size_predictor,
        #             k=50,
        #             num_requests=self.num_req_per_experiment,
        #             num_experiments=self.num_repetitions
        #         )
        #         rows.append([mean_nt, avg_E, ME])
        #     if self.verbose:
        #         print(rows)
        #     # write data to file
        #     results_file = self.results_folder_path + '/nt.txt'
        #     rows = pd.DataFrame(rows)
        #     rows.to_csv(results_file, header=False, index=False)
        #
        #
        #
        #
        # ###############################
        # ### Access time experiment ###
        # ###############################
        # access_times = [1, 5, 10, 15, 20]
        # if self.perform_at_experiments:
        #     rows = []
        #     for access_time in access_times:
        #         print("access_time experiment: at=" + str(access_time))
        #         device_service_time_creator = Storage_with_access_time_and_blocks_st(access_time=access_time,
        #                                                                              transfer_rate=default_transfer_rate,
        #                                                                              block_size=default_block_size)
        #         avg_E, ME = Simulator.simulate(
        #             arrival_times_creator=default_arrival_times_creator,
        #             network_delay_creator=default_network_delay_creator,
        #             batch_service_time_creator=device_service_time_creator,
        #             ia_predictor=self.ia_predictor,
        #             st_predictor=self.st_predictor,
        #             req_size_predictor=self.req_size_predictor,
        #             k=50,
        #             num_requests=self.num_req_per_experiment,
        #             num_experiments=self.num_repetitions
        #         )
        #         rows.append([access_time, avg_E, ME])
        #     if self.verbose:
        #         print(rows)
        #     # write data to file
        #     results_file = self.results_folder_path + '/at.txt'
        #     rows = pd.DataFrame(rows)
        #     rows.to_csv(results_file, header=False, index=False)
        #
        #
        # ################################
        # ### Transfer Rate experiment ###
        # ################################
        # transfer_rates = [40000, 60000, 80000, 100000]
        # if self.perform_tr_experiments:
        #     rows = []
        #     for transfer_rate in transfer_rates:
        #         print("transfer_rate experiment: tr=" + str(transfer_rate))
        #         device_service_time_creator = Storage_with_access_time_and_blocks_st(access_time=default_mean_at,
        #                                                                              transfer_rate=transfer_rate,
        #                                                                              block_size=default_block_size)
        #         avg_E, ME = Simulator.simulate(
        #             arrival_times_creator=default_arrival_times_creator,
        #             network_delay_creator=default_network_delay_creator,
        #             batch_service_time_creator=device_service_time_creator,
        #             ia_predictor=self.ia_predictor,
        #             st_predictor=self.st_predictor,
        #             req_size_predictor=self.req_size_predictor,
        #             k=50,
        #             num_requests=self.num_req_per_experiment,
        #             num_experiments=self.num_repetitions
        #         )
        #         rows.append([access_time, avg_E, ME])
        #     if self.verbose:
        #         print(rows)
        #     # write data to file
        #     results_file = self.results_folder_path + '/at.txt'
        #     rows = pd.DataFrame(rows)
        #     rows.to_csv(results_file, header=False, index=False)
        #
        #
        #
        #
        #
        # ###################################
        # ### Multiple Source Experiments ###
        # ###################################
        #
        # mean_inter_arrival_times = [100, 100]
        # if self.perform_num_sources_experiments:
        #     print("mean_inter_arrival_times " + str(mean_inter_arrival_times))
        #     rows = []
        #     arrival_times_creator = Multiple_sources_exponential_inter_arrival_times(mean_inter_arrival_times)
        #     avg_E, ME = Simulator.simulate(
        #         arrival_times_creator=arrival_times_creator,
        #         network_delay_creator=default_network_delay_creator,
        #         batch_service_time_creator=default_device_service_time_creator,
        #         ia_predictor=self.ia_predictor,
        #         st_predictor=self.st_predictor,
        #         req_size_predictor=self.req_size_predictor,
        #         k=50,
        #         num_requests=self.num_req_per_experiment,
        #         num_experiments=self.num_repetitions
        #     )
        #     res = []
        #     for mean_ia in mean_ias:
        #         res.append(mean_ia)
        #     res.append(avg_E)
        #     res.append(ME)
        #     rows.append(res)
        # if self.verbose:
        #     print(rows)
        #     # write data to file
        #     results_file = self.results_folder_path + "/sources" + str(num_sources) + '.txt'
        #     rows = pd.DataFrame(rows)
        #     rows.to_csv(results_file, header=False, index=False)

