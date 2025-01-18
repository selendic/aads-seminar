import os

# Dataset path and configurations
DATASET_PATH = lambda suffix: os.path.join(os.path.dirname(__file__), f"../resources/google-10000-english-usa-no-swears{suffix}.txt")
CSV_PATH = os.path.join(os.path.dirname(__file__), "csv/")
PLOT_PATH = os.path.join(os.path.dirname(__file__), "plots/")
PROFILE_OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "profiling/")
#MIN_WORD_LENGTH = 1
#MAX_WORD_LENGTH = sys.maxsize
INCREMENTAL_SIZES = [500 * i for i in range(1, 21)]  # [500, 1000, 1500, ..., 10000]
