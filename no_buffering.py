from ExperimentPerformer import ExperimentPerformer

results_folder_path = 'results/test'
#results_folder_path = 'results/no_buffering'
exp_p = ExperimentPerformer(
    results_folder_path=results_folder_path,
    num_req_per_experiment=50000,
    num_repetitions=30,
    ia_predictor=None,
    st_predictor=None,
    perform_ia_experiments=False,
    perform_nt_experiments=True,
    perform_st_experiments=False,
    perform_num_sources_experiments=False
)
exp_p.perform_experiment()



