from util.Constants import SAMPLES_OF_DATA_TO_LOOK_AT


def train():
    import numpy as np

    from models.CryptoPumpAndDumpDetector import CryptoPumpAndDumpDetector
    from models.Hyperparameters import Hyperparameters

    print("Loading dataset...")
    # pumps_df = pd.read_csv("../data_set/final-dataset-pumps.csv")
    # non_pumps_df = pd.read_csv("../data_set/final-dataset-non-pumps.csv")
    # all_df = pumps_df.append(non_pumps_df).reset_index(drop=True)
    # all_df = all_df.reindex(
    #     np.random.permutation(all_df.index))
    # numberOfEntries = len(all_df.index)

    pumps = []
    nonPumps = []

    import csv

    with open('../data_set/final-dataset-pumps.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        skip = True

        for row in reader:
            if skip:
                skip = False
                continue

            pump = []
            for i in range(SAMPLES_OF_DATA_TO_LOOK_AT):
                pump.append((float(row[i]), float(row[i + SAMPLES_OF_DATA_TO_LOOK_AT]),
                             float(row[i + SAMPLES_OF_DATA_TO_LOOK_AT * 2]),
                             float(row[i + SAMPLES_OF_DATA_TO_LOOK_AT * 3])))
                # pump.append((float(row[i]),))
                # pump.append(float(row[i]))

            pumps.append(np.array(pump))

    with open('../data_set/final-dataset-non-pumps.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        skip = True

        for row in reader:
            if skip:
                skip = False
                continue

            pump = []
            for i in range(SAMPLES_OF_DATA_TO_LOOK_AT):
                pump.append((float(row[i]), float(row[i + SAMPLES_OF_DATA_TO_LOOK_AT]),
                             float(row[i + SAMPLES_OF_DATA_TO_LOOK_AT * 2]),
                             float(row[i + SAMPLES_OF_DATA_TO_LOOK_AT * 3])))
                # pump.append((float(row[i]),))
                # pump.append(float(row[i]))

            nonPumps.append(np.array(pump))

    labels = [1 for i in range(len(pumps))] + [0 for i in range(len(nonPumps))]
    data = pumps + nonPumps
    indices = [i for i in range(len(pumps) + len(nonPumps))]
    np.random.shuffle(indices)
    labels = np.array([labels[i] for i in indices])
    data = np.array([data[i] for i in indices])
    print(data)

    # Hyperparameters!
    learningRate = 0.002
    epochs = 40
    batchSize = 3000
    labelName = "Pump"
    classificationThreshold = 0.5
    decayRate = 0.05
    decayStep = 1.0

    model = CryptoPumpAndDumpDetector(tryUsingGPU=True)
    model.setup(classificationThreshold,
                Hyperparameters(learningRate, epochs, batchSize,
                                decayRate=decayRate, decayStep=decayStep))

    model.createModelUsingDefaults()
    epochs, hist = model.trainModel(data, labels, 0.15)
    list_of_metrics_to_plot = model.listOfMetrics
    model.plotCurve(epochs, hist, list_of_metrics_to_plot)

    model.exportWeights()

    # features = {name: np.array(value) for name, value in test_df.items()}
    # label = np.array(features.pop(labelName))
    #
    #
    #
    # print(model.evaluate(features, label))
    # print(test_df.iloc[0])
    # #
    # # print("====== Predictions =======")
    # # tester = {'Volume-RA-0': [np.float32(-0.29340664)], 'Volume-RA-1': [np.float32(0.38819954)], 'Volume-RA-2': [np.float32(-0.29340664)], 'Volume-RA-3': [np.float32(-0.29340664)], 'Volume-RA-4': [np.float32(-0.29340664)], 'Volume-RA-5': [np.float32(-0.29340664)], 'Volume-RA-6': [np.float32(0.38819954)], 'Volume-RA-7': [np.float32(-0.29340664)], 'Volume-RA-8': [np.float32(-0.29340664)], 'Volume-RA-9': [np.float32(-0.29340664)], 'Volume-RA-10': [np.float32(-0.29340664)], 'Volume-RA-11': [np.float32(0.38819954)], 'Volume-RA-12': [np.float32(-0.29340664)], 'Volume-RA-13': [np.float32(-0.29340664)], 'Volume-RA-14': [np.float32(2.433018)], 'Volume-RA-15': [np.float32(-0.29340664)], 'Volume-RA-16': [np.float32(-0.29340664)], 'Volume-RA-17': [np.float32(-0.29340664)], 'Volume-RA-18': [np.float32(-0.29340664)], 'Volume-RA-19': [np.float32(-0.29340664)], 'Volume-RA-20': [np.float32(-0.29340664)], 'Volume-RA-21': [np.float32(-0.29340664)], 'Volume-RA-22': [np.float32(-0.29340664)], 'Volume-RA-23': [np.float32(-0.29340664)], 'Volume-RA-24': [np.float32(-0.29340664)], 'Volume-RA-25': [np.float32(-0.29340664)], 'Volume-RA-26': [np.float32(-0.29340664)], 'Volume-RA-27': [np.float32(-0.29340664)], 'Volume-RA-28': [np.float32(0.38819954)], 'Volume-RA-29': [np.float32(-0.29340664)], 'Volume-RA-30': [np.float32(-0.29340664)], 'Volume-RA-31': [np.float32(-0.29340664)], 'Volume-RA-32': [np.float32(-0.29340664)], 'Volume-RA-33': [np.float32(-0.29340664)], 'Volume-RA-34': [np.float32(-0.29340664)], 'Volume-RA-35': [np.float32(-0.29340664)], 'Volume-RA-36': [np.float32(-0.29340664)], 'Volume-RA-37': [np.float32(-0.29340664)], 'Volume-RA-38': [np.float32(-0.29340664)], 'Volume-RA-39': [np.float32(-0.29340664)], 'Volume-RA-40': [np.float32(-0.29340664)], 'Volume-RA-41': [np.float32(-0.29340664)], 'Volume-RA-42': [np.float32(1.0698057)], 'Volume-RA-43': [np.float32(0.38819954)], 'Volume-RA-44': [np.float32(-0.29340664)], 'Volume-RA-45': [np.float32(-0.29340664)], 'Volume-RA-46': [np.float32(1.7514119)], 'Volume-RA-47': [np.float32(-0.29340664)], 'Volume-RA-48': [np.float32(-0.29340664)], 'Volume-RA-49': [np.float32(-0.29340664)], 'Volume-RA-50': [np.float32(-0.29340664)], 'Volume-RA-51': [np.float32(1.7514119)], 'Volume-RA-52': [np.float32(-0.29340664)], 'Volume-RA-53': [np.float32(-0.29340664)], 'Volume-RA-54': [np.float32(0.38819954)], 'Volume-RA-55': [np.float32(-0.29340664)], 'Volume-RA-56': [np.float32(-0.29340664)], 'Volume-RA-57': [np.float32(-0.29340664)], 'Volume-RA-58': [np.float32(-0.29340664)], 'Volume-RA-59': [np.float32(-0.29340664)], 'Volume-RA-60': [np.float32(5.841049)], 'Volume-RA-61': [np.float32(0.38819954)], 'Volume-RA-62': [np.float32(-0.29340664)], 'Volume-RA-63': [np.float32(-0.29340664)], 'Volume-RA-64': [np.float32(-0.29340664)], 'Volume-RA-65': [np.float32(-0.29340664)], 'Volume-RA-66': [np.float32(3.7962306)], 'Volume-RA-67': [np.float32(-0.29340664)], 'Volume-RA-68': [np.float32(-0.29340664)], 'Volume-RA-69': [np.float32(-0.29340664)], 'Volume-RA-70': [np.float32(-0.29340664)], 'Volume-RA-71': [np.float32(-0.29340664)], 'Volume-RA-72': [np.float32(-0.29340664)], 'Volume-RA-73': [np.float32(-0.29340664)], 'Volume-RA-74': [np.float32(-0.29340664)], 'Volume-RA-75': [np.float32(-0.29340664)], 'Volume-RA-76': [np.float32(-0.29340664)], 'Volume-RA-77': [np.float32(-0.29340664)], 'Volume-RA-78': [np.float32(-0.29340664)], 'Volume-RA-79': [np.float32(-0.29340664)], 'Volume-RA-80': [np.float32(-0.29340664)], 'Volume-RA-81': [np.float32(-0.29340664)], 'Volume-RA-82': [np.float32(-0.29340664)], 'Volume-RA-83': [np.float32(-0.29340664)], 'Volume-RA-84': [np.float32(-0.29340664)], 'Volume-RA-85': [np.float32(2.433018)], 'Volume-RA-86': [np.float32(-0.29340664)], 'Volume-RA-87': [np.float32(-0.29340664)], 'Volume-RA-88': [np.float32(-0.29340664)], 'Volume-RA-89': [np.float32(0.38819954)], 'Volume-RA-90': [np.float32(-0.29340664)], 'Volume-RA-91': [np.float32(-0.29340664)], 'Volume-RA-92': [np.float32(-0.29340664)], 'Volume-RA-93': [np.float32(1.7514119)], 'Volume-RA-94': [np.float32(-0.29340664)], 'Volume-RA-95': [np.float32(-0.29340664)], 'Volume-RA-96': [np.float32(0.38819954)], 'Volume-RA-97': [np.float32(-0.29340664)], 'Volume-RA-98': [np.float32(-0.29340664)], 'Volume-RA-99': [np.float32(-0.29340664)], 'Volume-RA-100': [np.float32(-0.29340664)], 'Volume-RA-101': [np.float32(-0.29340664)], 'Volume-RA-102': [np.float32(-0.29340664)], 'Volume-RA-103': [np.float32(-0.29340664)], 'Volume-RA-104': [np.float32(-0.29340664)], 'Volume-RA-105': [np.float32(-0.29340664)], 'Volume-RA-106': [np.float32(-0.29340664)], 'Volume-RA-107': [np.float32(-0.29340664)], 'Volume-RA-108': [np.float32(-0.29340664)], 'Volume-RA-109': [np.float32(-0.29340664)], 'Volume-RA-110': [np.float32(-0.29340664)], 'Volume-RA-111': [np.float32(1.7514119)], 'Volume-RA-112': [np.float32(1.0698057)], 'Volume-RA-113': [np.float32(-0.29340664)], 'Volume-RA-114': [np.float32(-0.29340664)], 'Volume-RA-115': [np.float32(-0.29340664)], 'Volume-RA-116': [np.float32(0.38819954)], 'Volume-RA-117': [np.float32(0.38819954)], 'Volume-RA-118': [np.float32(-0.29340664)], 'Volume-RA-119': [np.float32(-0.29340664)], 'Volume-RA-120': [np.float32(-0.29340664)], 'Volume-RA-121': [np.float32(0.38819954)], 'Volume-RA-122': [np.float32(-0.29340664)], 'Volume-RA-123': [np.float32(-0.29340664)], 'Volume-RA-124': [np.float32(-0.29340664)], 'Volume-RA-125': [np.float32(-0.29340664)], 'Volume-RA-126': [np.float32(-0.29340664)], 'Volume-RA-127': [np.float32(-0.29340664)], 'Volume-RA-128': [np.float32(-0.29340664)], 'Volume-RA-129': [np.float32(-0.29340664)], 'Volume-RA-130': [np.float32(-0.29340664)], 'Volume-RA-131': [np.float32(-0.29340664)], 'Volume-RA-132': [np.float32(-0.29340664)], 'Volume-RA-133': [np.float32(-0.29340664)], 'Volume-RA-134': [np.float32(-0.29340664)], 'Volume-RA-135': [np.float32(-0.29340664)], 'Volume-RA-136': [np.float32(-0.29340664)], 'Volume-RA-137': [np.float32(-0.29340664)], 'Volume-RA-138': [np.float32(1.0698057)], 'Volume-RA-139': [np.float32(7.8858676)], 'Volume-RA-140': [np.float32(-0.29340664)], 'Volume-RA-141': [np.float32(-0.29340664)], 'Volume-RA-142': [np.float32(-0.29340664)], 'Volume-RA-143': [np.float32(-0.29340664)], 'Volume-RA-144': [np.float32(-0.29340664)], 'Volume-RA-145': [np.float32(-0.29340664)], 'Volume-RA-146': [np.float32(-0.29340664)], 'Volume-RA-147': [np.float32(-0.29340664)], 'Volume-RA-148': [np.float32(-0.29340664)], 'Volume-RA-149': [np.float32(-0.29340664)], 'Price-RA-0': [np.float32(-0.29340664)], 'Price-RA-1': [np.float32(-1.4002801)], 'Price-RA-2': [np.float32(0.361739)], 'Price-RA-3': [np.float32(0.361739)], 'Price-RA-4': [np.float32(0.361739)], 'Price-RA-5': [np.float32(0.361739)], 'Price-RA-6': [np.float32(0.361739)], 'Price-RA-7': [np.float32(2.123758)], 'Price-RA-8': [np.float32(2.123758)], 'Price-RA-9': [np.float32(2.123758)], 'Price-RA-10': [np.float32(2.123758)], 'Price-RA-11': [np.float32(2.123758)], 'Price-RA-12': [np.float32(0.361739)], 'Price-RA-13': [np.float32(0.361739)], 'Price-RA-14': [np.float32(0.361739)], 'Price-RA-15': [np.float32(0.361739)], 'Price-RA-16': [np.float32(0.361739)], 'Price-RA-17': [np.float32(0.361739)], 'Price-RA-18': [np.float32(0.361739)], 'Price-RA-19': [np.float32(0.361739)], 'Price-RA-20': [np.float32(0.361739)], 'Price-RA-21': [np.float32(0.361739)], 'Price-RA-22': [np.float32(0.361739)], 'Price-RA-23': [np.float32(0.361739)], 'Price-RA-24': [np.float32(0.361739)], 'Price-RA-25': [np.float32(0.361739)], 'Price-RA-26': [np.float32(0.361739)], 'Price-RA-27': [np.float32(0.361739)], 'Price-RA-28': [np.float32(0.361739)], 'Price-RA-29': [np.float32(0.361739)], 'Price-RA-30': [np.float32(0.361739)], 'Price-RA-31': [np.float32(0.361739)], 'Price-RA-32': [np.float32(0.361739)], 'Price-RA-33': [np.float32(0.361739)], 'Price-RA-34': [np.float32(0.361739)], 'Price-RA-35': [np.float32(0.361739)], 'Price-RA-36': [np.float32(0.361739)], 'Price-RA-37': [np.float32(0.361739)], 'Price-RA-38': [np.float32(0.361739)], 'Price-RA-39': [np.float32(0.361739)], 'Price-RA-40': [np.float32(0.361739)], 'Price-RA-41': [np.float32(0.361739)], 'Price-RA-42': [np.float32(0.361739)], 'Price-RA-43': [np.float32(0.361739)], 'Price-RA-44': [np.float32(0.361739)], 'Price-RA-45': [np.float32(0.361739)], 'Price-RA-46': [np.float32(0.361739)], 'Price-RA-47': [np.float32(0.361739)], 'Price-RA-48': [np.float32(0.361739)], 'Price-RA-49': [np.float32(0.361739)], 'Price-RA-50': [np.float32(0.361739)], 'Price-RA-51': [np.float32(0.361739)], 'Price-RA-52': [np.float32(-1.4002801)], 'Price-RA-53': [np.float32(-1.4002801)], 'Price-RA-54': [np.float32(-1.4002801)], 'Price-RA-55': [np.float32(-1.4002801)], 'Price-RA-56': [np.float32(-1.4002801)], 'Price-RA-57': [np.float32(-1.4002801)], 'Price-RA-58': [np.float32(-1.4002801)], 'Price-RA-59': [np.float32(-1.4002801)], 'Price-RA-60': [np.float32(-1.4002801)], 'Price-RA-61': [np.float32(3.8857772)], 'Price-RA-62': [np.float32(-1.4002801)], 'Price-RA-63': [np.float32(-1.4002801)], 'Price-RA-64': [np.float32(-1.4002801)], 'Price-RA-65': [np.float32(-1.4002801)], 'Price-RA-66': [np.float32(-1.4002801)], 'Price-RA-67': [np.float32(-1.4002801)], 'Price-RA-68': [np.float32(-1.4002801)], 'Price-RA-69': [np.float32(-1.4002801)], 'Price-RA-70': [np.float32(-1.4002801)], 'Price-RA-71': [np.float32(-1.4002801)], 'Price-RA-72': [np.float32(-1.4002801)], 'Price-RA-73': [np.float32(-1.4002801)], 'Price-RA-74': [np.float32(-1.4002801)], 'Price-RA-75': [np.float32(-1.4002801)], 'Price-RA-76': [np.float32(-1.4002801)], 'Price-RA-77': [np.float32(-1.4002801)], 'Price-RA-78': [np.float32(-1.4002801)], 'Price-RA-79': [np.float32(-1.4002801)], 'Price-RA-80': [np.float32(-1.4002801)], 'Price-RA-81': [np.float32(-1.4002801)], 'Price-RA-82': [np.float32(-1.4002801)], 'Price-RA-83': [np.float32(-1.4002801)], 'Price-RA-84': [np.float32(-1.4002801)], 'Price-RA-85': [np.float32(-1.4002801)], 'Price-RA-86': [np.float32(-1.4002801)], 'Price-RA-87': [np.float32(-1.4002801)], 'Price-RA-88': [np.float32(-1.4002801)], 'Price-RA-89': [np.float32(-1.4002801)], 'Price-RA-90': [np.float32(-1.4002801)], 'Price-RA-91': [np.float32(-1.4002801)], 'Price-RA-92': [np.float32(-1.4002801)], 'Price-RA-93': [np.float32(-1.4002801)], 'Price-RA-94': [np.float32(2.123758)], 'Price-RA-95': [np.float32(2.123758)], 'Price-RA-96': [np.float32(2.123758)], 'Price-RA-97': [np.float32(0.361739)], 'Price-RA-98': [np.float32(0.361739)], 'Price-RA-99': [np.float32(0.361739)], 'Price-RA-100': [np.float32(0.361739)], 'Price-RA-101': [np.float32(0.361739)], 'Price-RA-102': [np.float32(0.361739)], 'Price-RA-103': [np.float32(0.361739)], 'Price-RA-104': [np.float32(0.361739)], 'Price-RA-105': [np.float32(0.361739)], 'Price-RA-106': [np.float32(0.361739)], 'Price-RA-107': [np.float32(0.361739)], 'Price-RA-108': [np.float32(0.361739)], 'Price-RA-109': [np.float32(0.361739)], 'Price-RA-110': [np.float32(0.361739)], 'Price-RA-111': [np.float32(0.361739)], 'Price-RA-112': [np.float32(2.123758)], 'Price-RA-113': [np.float32(0.361739)], 'Price-RA-114': [np.float32(0.361739)], 'Price-RA-115': [np.float32(0.361739)], 'Price-RA-116': [np.float32(0.361739)], 'Price-RA-117': [np.float32(0.361739)], 'Price-RA-118': [np.float32(0.361739)], 'Price-RA-119': [np.float32(0.361739)], 'Price-RA-120': [np.float32(0.361739)], 'Price-RA-121': [np.float32(0.361739)], 'Price-RA-122': [np.float32(0.361739)], 'Price-RA-123': [np.float32(0.361739)], 'Price-RA-124': [np.float32(0.361739)], 'Price-RA-125': [np.float32(0.361739)], 'Price-RA-126': [np.float32(0.361739)], 'Price-RA-127': [np.float32(0.361739)], 'Price-RA-128': [np.float32(0.361739)], 'Price-RA-129': [np.float32(0.361739)], 'Price-RA-130': [np.float32(0.361739)], 'Price-RA-131': [np.float32(0.361739)], 'Price-RA-132': [np.float32(0.361739)], 'Price-RA-133': [np.float32(0.361739)], 'Price-RA-134': [np.float32(0.361739)], 'Price-RA-135': [np.float32(0.361739)], 'Price-RA-136': [np.float32(0.361739)], 'Price-RA-137': [np.float32(0.361739)], 'Price-RA-138': [np.float32(0.361739)], 'Price-RA-139': [np.float32(0.361739)], 'Price-RA-140': [np.float32(0.361739)], 'Price-RA-141': [np.float32(0.361739)], 'Price-RA-142': [np.float32(0.361739)], 'Price-RA-143': [np.float32(0.361739)], 'Price-RA-144': [np.float32(0.361739)], 'Price-RA-145': [np.float32(0.361739)], 'Price-RA-146': [np.float32(0.361739)], 'Price-RA-147': [np.float32(0.361739)], 'Price-RA-148': [np.float32(0.361739)], 'Price-RA-149': [np.float32(0.361739)]}
    # # model.detect(tester)


if __name__ == "__main__":
    train()
