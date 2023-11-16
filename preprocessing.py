
import pandas as pd
import pm4py
import time
import os

import datetime


def compute_duration(df, dataset_name):
    # Column names
    caseIdColName = "Case ID"
    durationColName = "Duration"
    timeStampColName = "Complete Timestamp"

    # Convert the entire 'Complete Timestamp' column to datetime format if it's not already
    if not isinstance(df[timeStampColName].iloc[0], pd.Timestamp):
        df[timeStampColName] = pd.to_datetime(
            df[timeStampColName], format='%Y/%m/%d %H:%M:%S.%f')

    # Initialize an empty list to store computed durations
    durations = []
    currentCase = ""
    oldTimeStamp = None

    for index, row in df.iterrows():
        newTimeStamp = row[timeStampColName]
        if dataset_name != "bpic2017":
            if currentCase != row[caseIdColName]:
                currentCase = row[caseIdColName]
                duration = 0.0
            else:
                duration = (newTimeStamp - oldTimeStamp).total_seconds()
            oldTimeStamp = newTimeStamp
        else:
            # Since startTimeStamp and endTimeStamp are the same in this block, duration will always be 0.0
            duration = 0.0

        durations.append(duration)

    # Add the computed durations as a new column to the DataFrame
    df[durationColName] = durations
    return df


times = {}

event_logs = {
    # "bpic2011": {"file_path": "logs/bpic2011/log.xes", "change_params": {'case:concept:name': 'Case ID', 'concept:name': 'Activity', 'time:timestamp': 'Complete Timestamp'}},
    "bpic2013": {"file_path": "logs/bpic2013/log.xes", "change_params": {'case:concept:name': 'Case ID', 'concept:name': 'Activity', 'time:timestamp': 'Complete Timestamp'}},
    "sepsis": {"file_path": "logs/sepsis/log.xes", "change_params": {'case:concept:name': 'Case ID', 'concept:name': 'Activity', 'time:timestamp': 'Complete Timestamp'}},
    "CoSeLoG": {"file_path": "logs/CoSeLoG/log.xes", "change_params": {'case:concept:name': 'Case ID', 'concept:name': 'Activity', 'time:timestamp': 'Complete Timestamp'}},
    # "Hospital_billings": {"file_path": "logs/Hospital_billings/log.xes", "change_params": {'case:concept:name': 'Case ID', 'concept:name': 'Activity', 'time:timestamp': 'Complete Timestamp'}},
    # "traffic_fines": {"file_path": "logs/traffic_fines/log.xes", "change_params": {'case:concept:name': 'Case ID', 'concept:name': 'Activity', 'time:timestamp': 'Complete Timestamp'}},
}

for current_log in event_logs.keys():
    print("Processing log: ", current_log)

    times[current_log] = {}
    times[current_log]["log"] = current_log

    start_time = time.time()

    filePath = event_logs[current_log]["file_path"]
    log = pm4py.read_xes(filePath)
    times[current_log]["read_xes"] = time.time() - start_time

    event_log = pm4py.convert_to_dataframe(log)

    case_ids_with_nan = event_log[event_log['concept:name'].isna(
    )]['case:concept:name'].unique()

    event_log = event_log[~event_log['case:concept:name'].isin(
        case_ids_with_nan)]

    variants_count = pm4py.get_variants(event_log)

    filtered_log = pm4py.filtering.filter_variants(
        event_log, [variant for variant, count in variants_count.items() if count > 1])
    filtered_log = pm4py.convert_to_dataframe(filtered_log)

    filtered_variants_count = pm4py.get_variants(filtered_log)
    print(filtered_variants_count)
    start_time = time.time()
    filtered_log.to_csv(filePath.replace("xes", "csv"))
    print("Number of filtered variants:", len(
        variants_count) - len(filtered_variants_count))

    dataframe = filtered_log

    dataframe = dataframe.rename(
        columns=event_logs[current_log]["change_params"])
    dataframe.to_csv(filePath.replace(".xes", "_pretsaColName.csv"))
    times[current_log]["change_column_names"] = time.time() - start_time
    start_time = time.time()

    dataframe = compute_duration(dataframe, "sepsis")

    case_ids_with_nan = dataframe[dataframe['Activity'].isna(
    )]['Case ID'].unique()
    case_ids_with_nan += dataframe[dataframe['Complete Timestamp'].isna()
                                   ]['Case ID'].unique()

    dataframe = dataframe[~dataframe['Case ID'].isin(case_ids_with_nan)].copy()

    dataframe.to_csv(filePath.replace(".xes", "_duration.csv"), sep=";")
    times[current_log]["compute_duration"] = time.time() - start_time

    file_path = os.path.join("logs/prep.txt")
    with open(file_path, 'w') as f:
        for item in times.values():
            f.write("%s\n" % item)
