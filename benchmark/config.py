# Dataset path and configurations
DATASET_PATH = lambda suffix: f"../resources/google-10000-english-usa-no-swears{suffix}.txt"
CSV_PATH = "csv/experiment_results.csv"
PLOT_PATH = "plots/"
PROFILE_OUTPUT_PATH = "profiling/output.txt"
#MIN_WORD_LENGTH = 1
#MAX_WORD_LENGTH = sys.maxsize
INCREMENTAL_SIZES = [500 * i for i in range(1, 21)]  # [500, 1000, 1500, ..., 10000]
