The code is written in Python 3.13 and uses the libraries listed in the requirements.txt file using a virtual environment (venv).
To create a new virtual environment, run the following command:
```bash
python -m venv venv
```

To activate the virtual environment on macOS and Linux, run the following command:
```bash
source venv/bin/activate
```
and on Windows:
```bash
venv\Scripts\activate
```

To install the required libraries, run the following command:
```bash
pip install -r requirements.txt
```

The trie implementations lie in trie/ folder.
To run the unit tests, run the following command:
```bash
python -m unittest discover
```

To run the benchmarking experiments, run the following command:
```bash
python benchmark/run_experiments.py
```
And to run the profiler, run the following command:
```bash
python benchmark/run_profiling.py
```
