# Performance Comparison of a (Prefix) Trie and Patricia Trie

This repository contains the implementation and performance comparison of a Prefix Trie and a Patricia Trie as part of the **Advanced Algorithms and Data Structures** course at the Faculty of Electrical Engineering and Computing, University of Zagreb.

The project aims to:
- Implement the Prefix Trie and the Patricia Trie with the possibility if visualization at any steps.
- Provide instructions to set up and run the code.
- Include datasets for benchmarking experiments.
- Compare the time and memory complexity of insert, search, range-search, and delete operations over incremental dataset sizes.
- Present results with performance graphs, discuss findings, and analyze any deviations from expected results.

---

## **Getting Started**

### Prerequisites
This project is written in **Python 3.13**. Running on lower versions could work, but Python 3.13 or higher is recommended.

### Setting Up a Virtual Environment
It is recommended to use a virtual environment to manage dependencies. To create and activate a virtual environment, follow these steps:

#### Linux and macOS
```bash
python -m venv venv
source venv/bin/activate
```

#### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

### Installing Dependencies
Install the required Python libraries listed in the `requirements.txt` file by running:
```bash
pip install -r requirements.txt
```

---

## **Repository Structure**
- **`benchmark/`**: Scripts for running benchmarking experiments and profiling.
- **`document/`**: LaTeX and PDF files for the seminar document.
- **`resources/`**: Datasets used for testing and benchmarking the implementations.
- **`test/`**: Unit tests for the implementations.
- **`trie/`**: Contains the implementations of Prefix and Patricia Tries.
- **`requirements.txt`**: Lists the required Python libraries.

---

## **Usage**

### Running Unit Tests
To ensure the correctness of the implementations, a few unit tests are provided. Run the tests with:
```bash
python -m unittest discover
```

### Running Benchmarking Experiments
Run the experiments to measure performance across various dataset sizes with:
```bash
python benchmark/run_experiments.py
```

### Running the Profiler
To confirm the experiment results by profiling the implementation and analyzing its performance in more detail, use:
```bash
python benchmark/run_profiling.py
```

---

## **Acknowledgments**
This work is part of the **Advanced Algorithms and Data Structures** course at the Faculty of Electrical Engineering and Computing, University of Zagreb.
Special thanks to course instructors for their valuable guidance.

---

## **Contact**
For any inquiries or feedback, feel free to reach out:
- **Name**: Marko Šelendić
- **Email**: marko.selendic@fer.hr

---
