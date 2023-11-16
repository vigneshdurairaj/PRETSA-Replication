# PRETSA-Replication
This repository contains the replication code and analysis for the research conducted by Fahrenkrog-Petersen et al.,[^1] focused on PRETSA algorithms in process mining for privacy preservation. The original study introduced PRETSA BF and PRETSA STAR, tested on real-life event logs.
This work is a replication of the PRETSA research. Original GitHub repository: PRETSA Original Repository : [Link](https://github.com/samadeusfp/PRETSA)


## Implementation Details
Our replication follows the methodology of the original study, extending it to additional datasets, including BPIC 2011. The repository includes scripts for preprocessing, analysis, and evaluation of the algorithms' performance and impact on data privacy.

## Dataset and Preprocessing
The replication involved datasets such as Traffic Fines, Hospital Billing, CoSeLog, BPIC 2013, Sepsis, BPIC 2011. Preprocessing steps included calculation of event durations, renaming columns, and converting event logs to compatible formats.

## Experiment Setup and Execution
The replication study aims to validate the performance and utility preservation of the PRETSA suite. We conducted detailed runtime and utility analyses.
The replication process is structured as follows:

1. **Log Placement**: Place the event logs in a directory named `logs`. Duplicate the template folder for each new event log.
2. **Log File Naming**: Replace the `log.xes` file in each folder with your event log file, keeping the filename `log.xes`.
3. **Preprocessing Step**: Process the logs for the PRETSA algorithms using the `preprocessing.py` script.
4. **Algorithm Execution**: Run the `run_algorithms.py` script to execute the algorithms. Specify the logs, algorithms, and values for parameters `k` and `t`.
5. **Output Files**: The sanitized event logs and execution insights are saved in the format: 
   - `logs/LOG_NAME/ALGORITHM/logs/log_duration_t{tvalue}_k{kvalue}_ALGORITHM.csv`
   - `logs/LOG_NAME/ALGORITHM/pickles/log_duration_t{tvalue}_k{kvalue}_ALGORITHM.pickle`.
   Replace `LOG_NAME`, `ALGORITHM`, `{tvalue}`, and `{kvalue}` with your specific identifiers.
6. **Analysis Execution**: Run the `analysis.ipynb` Jupyter notebook for analysis. Use `analysis_helper.ipynb` to format the `.pickle` files beforehand.

Important: To successfully replicate the experiment across all six event logs, including BPIC 2011, Traffic Fines, and Hospital Billings, it's necessary to have the respective .xes files in their designated folders. Please download these files from the sources cited and place them as instructed in the earlier sections. If this step is ignored, the replication will run on the other three event logs(included in this repository) without any errors.

### Data Sources
The following datasets were used in the replication study:

- CoSeLog: [DOI: 10.4121/uuid:a07386a5-7be3-4367-9535-70bc9e77dbe6](https://doi.org/10.4121/uuid:a07386a5-7be3-4367-9535-70bc9e77dbe6)
- BPIC 2011: [DOI: 10.4121/uuid:d9769f3d-0ab0-4fb8-803b-0d1120ffcf54](https://doi.org/10.4121/uuid:d9769f3d-0ab0-4fb8-803b-0d1120ffcf54)
- Traffic Fines: [DOI: 10.4121/uuid:270fd440-1057-4fb9-89a9-b699b47990f5](https://doi.org/10.4121/uuid:270fd440-1057-4fb9-89a9-b699b47990f5)
- Hospital Billings: [DOI: 10.4121/uuid:76c46b83-c930-4798-a1c9-4be94dfeb741](https://doi.org/10.4121/uuid:76c46b83-c930-4798-a1c9-4be94dfeb741)
- BPIC 2013: [DOI: 10.4121/uuid:500573e6-accc-4b0c-9576-aa5468b10cee](https://doi.org/10.4121/uuid:500573e6-accc-4b0c-9576-aa5468b10cee)
- Sepsis: [DOI: 10.4121/uuid:915d2bfb-7e84-49ad-a286-dc35f063a460](https://doi.org/10.4121/uuid:915d2bfb-7e84-49ad-a286-dc35f063a460)


[^1]: Fahrenkrog-Petersen, S.A., van der Aa, H. and Weidlich, M., 2023. Optimal event log sanitization for privacy-preserving process mining. Data & Knowledge Engineering, 145, p.102175.




