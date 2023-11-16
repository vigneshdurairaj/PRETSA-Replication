import pickle
from pretsa_star import Pretsa_star
from pretsa import Pretsa
import sys
import pandas as pd
import profile
import time


def modify_path(input_path, change):

    parts = input_path.split('/')
    parts.insert(-1, change)
    modified_path = '/'.join(parts)

    return modified_path


def perform_pretsa(k, t, masterFilePath, algo, ):

    pretsa, pretsa_bf, pretsa_star = False, False, False
    runtimes = {}

    if algo == "pretsa":
        pretsa = True
    elif algo == "pretsa_bf":
        pretsa_bf = True
    elif algo == "pretsa_star":
        pretsa_star = True
    else:
        print("Invalid algorithm")
        return None

    s = "k=%s, t=%s" % (k, t)

    sys.setrecursionlimit(300)
    filePath = masterFilePath.replace(".xes", "_duration.csv")

    if pretsa:
        targetFilePath = modify_path(
            filePath, "pretsa/logs").replace(".csv", "_t%s_k%s_pretsa.csv" % (t, k))
    elif pretsa_bf:
        targetFilePath = modify_path(
            filePath, "pretsa_bf/logs").replace(".csv", "_t%s_k%s_heuristic_pretsa.csv" % (t, k))
    elif pretsa_star:
        targetFilePath = modify_path(
            filePath, "pretsa_star/logs").replace(".csv", "_t%s_k%s_pretsa_star.csv" % (t, k))

    print("Load Event Log")
    eventLog = pd.read_csv(filePath, delimiter=";")

    print("Starting experiments")
    exp_start = time.time()
    if pretsa:
        pretsa = Pretsa(eventLog)
    elif pretsa_bf:
        pretsa_bf = Pretsa_star(eventLog, greedy=True)
    elif pretsa_star:
        pretsa_star = Pretsa_star(eventLog, greedy=False)
    exp_time = time.time() - exp_start
    print("Experiment took " + str(exp_time) + " seconds")
    s += ", exp_time=%s" % exp_time
    runtimes["exp_time"] = exp_time

    pretsa_start = time.time()
    if pretsa:
        cutOutCases, distanceLog = pretsa.runPretsa(int(k), float(t))
        print("Modified " + str(len(cutOutCases)) + " cases for k=" + str(k))
        s += ", cutOutCases=%s" % len(cutOutCases)
    elif pretsa_bf:
        cutOutCases, distanceLog = pretsa_bf.runPretsa(int(k), float(t))
        print("Modified " + str(len(cutOutCases)) + " cases for k=" + str(k))
        s += ", cutOutCases=%s" % len(cutOutCases)
    elif pretsa_star:
        cutOutCases, distanceLog = pretsa_star.runPretsa(int(k), float(t))
        print("Modified " + str(len(cutOutCases)) + " cases for k=" + str(k))
        s += ", cutOutCases=%s" % len(cutOutCases)

    pretsa_time = time.time() - pretsa_start
    print("Pretsa took " + str(pretsa_time) + " seconds")
    s += ", pretsa_time=%s" % pretsa_time
    runtimes["pretsa_time"] = pretsa_time

    private_start = time.time()
    if pretsa:
        privateEventLog = pretsa.getPrivatisedEventLog()
    elif pretsa_bf:
        privateEventLog = pretsa_bf.getPrivatisedEventLog()
    elif pretsa_star:
        privateEventLog = pretsa_star.getPrivatisedEventLog()

    private_time = time.time() - private_start
    print("Private event log took " + str(private_time) + " seconds")

    runtimes["private_time"] = private_time

    targetFilePathPickle = targetFilePath.replace(
        "/logs/", "/pickels/").replace(".csv", ".pickle")
    pickle.dump({"runtimes": runtimes, "cases": cutOutCases, "inflictedChanges": distanceLog, "time": (
        exp_time+pretsa_time+private_time)}, open(targetFilePathPickle, "wb"))
    print("Saved pickle to " + targetFilePathPickle)

    privateEventLog.to_csv(targetFilePath, sep=";", index=False)
    print("Saved private event log to " + targetFilePath)

    return s


ks = [4, 8, 16, 32, 64]
ts = [1, 2, 3, 4, 5]

algos = [
    "pretsa",
    "pretsa_bf",
    "pretsa_star"
]

event_logs = {
    "bpic2011": {"file_path": "logs/bpic2011/log.xes", },
    "bpic2013": {"file_path": "logs/bpic2013/log.xes", },
    "sepsis": {"file_path": "logs/sepsis/log.xes", },
    "CoSeLoG": {"file_path": "logs/CoSeLoG/log.xes", },
    # "Hospital_billings": {"file_path": "logs/Hospital_billings/log.xes", },
    # "traffic_fines": {"file_path": "logs/traffic_fines/log.xes", },
}

for al in algos:
    for current_log in event_logs.keys():

        masterFilePath = event_logs[current_log]["file_path"]

        for k in ks:

            for t in ts:

                print("Processing log: ", current_log)
                print("Algorithm: ", al)
                print("k: ", k)
                print("t: ", t)
                perform_pretsa(k, t, masterFilePath, al)
