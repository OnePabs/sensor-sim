import pickle
from ExperimentPerformer import ExperimentPerformer

linear_ia_predictor_path = 'ml_models/compressed_models/linear_ia_predictor.pkl'
with open(linear_ia_predictor_path, 'rb') as f:
    ia_predictor = pickle.load(f)

linear_st_predictor_path = 'ml_models/compressed_models/linear_st_predictor.pkl'
with open(linear_st_predictor_path, 'rb') as f:
    st_predictor = pickle.load(f)

results_folder_path = 'results/linear'
exp_p = ExperimentPerformer(
    results_folder_path=results_folder_path,
    num_req_per_experiment=10000,
    num_repetitions=30,
    ia_predictor=ia_predictor,
    st_predictor=st_predictor,
    perform_ia_experiments=True,
    perform_nt_experiments=True,
    perform_st_experiments=True,
    perform_num_sources_experiments=True
)
exp_p.perform_experiment()



