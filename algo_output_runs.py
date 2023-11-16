import pandas as pd
import os
from calculateSEDBetweenEventLogs import get_sed_between_logs
import statistics
import pickle


def get_mean_cycle_times(filePath):
    eventLog = pd.read_csv(filePath, delimiter=";")
    mean_cycle_times = eventLog.groupby('Activity').Duration.agg("mean")
    return mean_cycle_times


base_dirs = [
    'logs/bpic2011',
    'logs/bpic2013',
    'logs/CoSeLoG',
    # 'logs/Hospital_billings',
    'logs/sepsis',
    # 'logs/traffic_fines',
]


picks = []
for dir_path in base_dirs:

    filePathOriginalLog = dir_path+"/log_duration.csv"
    # print(filePathOriginalLog)

    event_log_original = pd.read_csv(filePathOriginalLog, delimiter=";")
    distanceMatrix = dict()
    original_cycle_time = get_mean_cycle_times(filePathOriginalLog)

    for k in (4, 8, 16, 32, 64):
        for t in (1, 2, 3, 4, 5):
            for algorithm in ("pretsa", "heuristic_pretsa", "pretsa_star"):
                data = dict()
                als = algorithm if algorithm != "heuristic_pretsa" else "pretsa_bf"
                filePathAlgoLog = dir_path + "/" + als+"/logs/log_duration_t" + \
                    str(t) + "_k" + str(k) + "_" + algorithm + ".csv"
                filePathAlgoPickel = dir_path + "/" + als+"/pickels/log_duration_t" + \
                    str(t) + "_k" + str(k) + "_" + algorithm + ".pickle"
                # print(filePathAlgoLog)

                # retained_varaints

                # Modified cases
                # print(filePathAlgoPickel)
                if os.path.exists(filePathAlgoPickel):
                    file = open(filePathAlgoPickel, 'rb')
                    pickle_data = pickle.load(file)
                    file.close()
                    data["cases"] = pickle_data["cases"]
                    data["cases_nr"] = len(pickle_data["cases"])
                    data["inflictedChanges"] = pickle_data["inflictedChanges"]
                else:
                    data = dict()
                    data["cases"] = -1
                    data["cases_nr"] = -1
                    data["inflictedChanges"] = -1

                # SED, Mean Cycle Time

                # print(filePathAlgoLog)
                if os.path.exists(filePathAlgoLog):
                    data["sed"] = \
                        get_sed_between_logs(
                            event_log_original, filePathAlgoLog, distanceMatrix)
                    errors = list()
                    log_cycle_times = get_mean_cycle_times(filePathAlgoLog)
                    for activity in original_cycle_time.keys():
                        originalValue = original_cycle_time[activity]
                        if originalValue != 0.0:
                            algorithmValue = log_cycle_times.get(activity, 0.0)
                            relativeError = abs(
                                (algorithmValue / originalValue) - 1.0)
                            if relativeError > 1:
                                relativeError = 1
                            errors.append(relativeError)
                    data["error"] = statistics.mean(errors)

                else:
                    data["sed"] = -1
                    data["error"] = -1

                data["k"] = k
                data["t"] = t
                data["algorithm"] = algorithm
                data["dataset"] = dir_path.split("/")[-1]

                picks.append(data)

    with open("algo_output_comparision.pickle", 'wb') as f:
        pickle.dump(picks, f)
