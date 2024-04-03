from common.Simulator import Simulator
from common.ArrivalTimesCreator import *
from common.RequestSizeCreator import *
from common.BatchServiceTimesCreator import *
import pandas as pd


class ExperimentPerformer:
    def __init__(
            self,
            results_folder_path,
            verbose=False,
            num_req_per_experiment=10000,
            num_repetitions=30,
            ia_predictor=None,
            st_predictor=None,
            perform_ia_experiments=True,
            perform_nt_experiments=True,
            perform_st_experiments=True,
            perform_num_sources_experiments=True
    ):
        self.results_folder_path = results_folder_path
        self.verbose = verbose
        self.num_req_per_experiment = num_req_per_experiment
        self.num_repetitions = num_repetitions
        self.ia_predictor = ia_predictor
        self.st_predictor = st_predictor
        self.perform_ia_experiments = perform_ia_experiments
        self.perform_nt_experiments = perform_nt_experiments
        self.perform_st_experiments = perform_st_experiments
        self.perform_num_sources_experiments = perform_num_sources_experiments


    def perform_experiment(self):
        default_mean_ia = 50
        default_mean_nt = 4
        default_mean_st = 40

        #######################
        #### IA experiments ###
        #######################
        mean_ias = [1000/10, 1000/15, 1000/20, 1000/22]
        if self.perform_ia_experiments:
            print("IA experiments")
            print("default network delay: " + str(default_mean_nt))
            print("default service time: " + str(default_mean_st))
            network_delay_distribution = Exponential_st(default_mean_nt)
            service_times_distribution = Exponential_st(default_mean_st)
            rows = []
            for mean_ia in mean_ias:
                print("ia=" + str(mean_ia))
                arrival_time_distribution = Poisson(mean_ia)
                avg_E, ME = Simulator.simulate(
                    arrival_time_distribution=arrival_time_distribution,
                    network_delay_creator=network_delay_distribution,
                    batch_service_time_creator=service_times_distribution,
                    ia_predictor=self.ia_predictor,
                    st_predictor=self.st_predictor,
                    num_ia_per_input=50,
                    num_batches_per_input=50,
                    num_requests=self.num_req_per_experiment,
                    num_experiments=self.num_repetitions
                )
                rows.append([mean_ia, avg_E, ME])
            if self.verbose:
                print(rows)
            # write data to file
            results_file = self.results_folder_path + '/ia.txt'
            rows = pd.DataFrame(rows)
            rows.to_csv(results_file, header=False, index=False)




        #################################
        ### Network delay experiments ###
        #################################
        mean_nts = [10] #[0, 2, 4, 6, 8, 10]
        if self.perform_nt_experiments:
            print("Network Delay experiments")
            print("default IA: " + str(default_mean_ia))
            print("default service time: " + str(default_mean_st))
            arrival_time_distribution = Poisson(default_mean_ia)
            service_times_distribution = ServiceTimeExponentialBatchSizeIndependent(default_mean_st)
            rows = []
            for mean_nt in mean_nts:
                print("NT experiment: nt=" + str(mean_nt))
                network_delay_distribution = ServiceTimeExponentialBatchSizeIndependent(mean_nt)
                avg_E, ME = Simulator.simulate(
                    arrival_time_distribution=arrival_time_distribution,
                    network_delay_creator=network_delay_distribution,
                    batch_service_time_creator=service_times_distribution,
                    ia_predictor=self.ia_predictor,
                    st_predictor=self.st_predictor,
                    num_ia_per_input=50,
                    num_batches_per_input=50,
                    num_requests=self.num_req_per_experiment,
                    num_experiments=self.num_repetitions
                )
                rows.append([mean_nt, avg_E, ME])
            if self.verbose:
                print(rows)
            # write data to file
            results_file = self.results_folder_path + '/nt.txt'
            rows = pd.DataFrame(rows)
            rows.to_csv(results_file, header=False, index=False)





        ###############################
        ### Service time experiment ###
        ###############################
        mean_sts = [1000/22, 1000/25, 1000/30, 1000/35]
        if self.perform_st_experiments:
            print("Service Times experiments")
            print("default IA: " + str(default_mean_ia))
            print("default network delay: " + str(default_mean_nt))
            arrival_time_distribution = Poisson(default_mean_ia)
            network_delay_distribution = ServiceTimeExponentialBatchSizeIndependent(default_mean_nt)
            rows = []
            for mean_st in mean_sts:
                print("ST experiment: st=" + str(mean_st))
                service_times_distribution = ServiceTimeExponentialBatchSizeIndependent(mean_st)
                avg_E, ME = Simulator.simulate(
                    arrival_time_distribution=arrival_time_distribution,
                    network_delay_creator=network_delay_distribution,
                    batch_service_time_creator=service_times_distribution,
                    ia_predictor=self.ia_predictor,
                    st_predictor=self.st_predictor,
                    num_ia_per_input=50,
                    num_batches_per_input=50,
                    num_requests=self.num_req_per_experiment,
                    num_experiments=self.num_repetitions
                )
                rows.append([mean_st, avg_E, ME])
            if self.verbose:
                print(rows)
            # write data to file
            results_file = self.results_folder_path + '/st.txt'
            rows = pd.DataFrame(rows)
            rows.to_csv(results_file, header=False, index=False)



        ###################################
        ### Multiple Source Experiments ###
        ###################################
        num_sources = 2
        mean_ias_per_experiment = [[84, 84], [84, 168]]
        if self.perform_num_sources_experiments:
            print("Num Sources experiment with " + str(num_sources) + " sources")
            print("default network delay: " + str(default_mean_nt))
            print("default service time: " + str(default_mean_st))
            network_delay_distribution = ServiceTimeExponentialBatchSizeIndependent(default_mean_nt)
            service_times_distribution = ServiceTimeExponentialBatchSizeIndependent(default_mean_st)
            rows = []
            for mean_ias in mean_ias_per_experiment:
                print("Experiment with sources mean inter-arrival times:")
                for i in range(num_sources):
                    print("Source: " + str(i) + "     mean_ia: " + str(mean_ias[i]))
                arrival_time_distribution = MultipleSourcesPoisson(num_sources, mean_ias)
                avg_E, ME = Simulator.simulate(
                    arrival_time_distribution=arrival_time_distribution,
                    network_delay_creator=network_delay_distribution,
                    batch_service_time_creator=service_times_distribution,
                    ia_predictor=self.ia_predictor,
                    st_predictor=self.st_predictor,
                    num_ia_per_input=50,
                    num_batches_per_input=50,
                    num_requests=self.num_req_per_experiment,
                    num_experiments=self.num_repetitions
                )
                res = []
                for mean_ia in mean_ias:
                    res.append(mean_ia)
                res.append(avg_E)
                res.append(ME)
                rows.append(res)
            if self.verbose:
                print(rows)
            # write data to file
            results_file = self.results_folder_path + "/sources" + str(num_sources) + '.txt'
            rows = pd.DataFrame(rows)
            rows.to_csv(results_file, header=False, index=False)





