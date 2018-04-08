from PerceptronVoted import PerceptronVoted
from PerceptronSimple import PerceptronSimple
from DatasetsFactory import DatasetsFactory
import datetime
import matplotlib.pyplot as plt
import time


def get_perceptron():
    if use_voted:
        return PerceptronVoted()
    else:
        return PerceptronSimple()


def abs(number):
    if number == 0:
        return number
    if number < 0:
        return number * -1
    return number


def testData(x, y, ephocs, to_predict, labels):
    if len(y) != len(x):
        print("Dataset error: having {0} x and {1} y".format(len(x), len(y)))
        return -1
    print("Train: ", len(x), "Test: ", len(to_predict), "Ephocs: ", ephocs)
    my_perceptron = get_perceptron()
    my_perceptron.train(x, y, ephocs)
    err = 0
    i = len(to_predict)
    for d, p in zip(to_predict, labels):
        result = my_perceptron.predict(d)
        if abs(result - p) != 0:
            err += 1
        i -= 1
        # print(i)
    errors = (err / len(to_predict) * 100)
    print("Accurancy: ", 100 - errors, "%")
    return 100 - errors


def plot_data(tests):
    plotdtx = []
    plotdty = []
    for test in tests:
        plotdtx.append(test[0])
        plotdty.append(test[3])
    plt.plot(plotdtx, plotdty, 'ob-')
    plt.ylabel('Errors')
    plt.xlabel('Ephocs')
    plt.show()


def save_results(tests, dataset, best):
    now = datetime.datetime.now()
    path = "results\\Log " + now.strftime("%Y-%m-%d %H %M %S") + " " + dataset['name'] + ".data"
    with open(path, "w+") as text_file:
        text_file.write("Dataset: " + dataset['name'] + "\n")
        text_file.write("Ephocs, Test, Train, Accurancy, Time")
        for test in tests:
            print(str(test))
            text_file.write("\n" + str(test).replace("[", "").replace("]", ""))
        text_file.write("\n\nBest:\n")
        text_file.write("Ephocs, Test, Train, Accurancy, Time\n")
        text_file.write(str(best['ephoc']) + "," + str(best['test_len']) + "," + str(best['train_len']) + "," + str(
            best['train_len']) + "," + str(best['time']))

# SETTINGS vars
dataPath = "datasets"
to_plot = False
use_voted = True
ephocs_train = [1, 3, 5, 10, 15, 20]
train_vector = [50, 80, 100, 150, 200]
test = 2500  # max testing number (many datasets could have <2500 data)

# main array of datasets
datasets = []
datasets.append({'name': 'simple_separable',
                 'data_train': DatasetsFactory.simple_points,
                 'data_test': DatasetsFactory.simple_points,
                 'train_path': '\\simple_points\\simple_points.data',
                 'test_path': '\\simple_points\\simple_points.data'})
datasets.append({'name': 'diseased_trees',
                 'data_train': DatasetsFactory.diseasedTrees,
                 'data_test': DatasetsFactory.diseasedTrees,
                 'train_path': '\\wilt\\training.csv',
                 'test_path': '\\wilt\\testing.csv'})
datasets.append({'name': 'iris',
                 'data_train': DatasetsFactory.iris,
                 'data_test': DatasetsFactory.iris,
                 'train_path': '\\iris\\iris.data',
                 'test_path': '\\iris\\iris.data'})
datasets.append({'name': 'cmc',
                 'data_train': DatasetsFactory.cmc,
                 'data_test': DatasetsFactory.cmc,
                 'train_path': '\\cmc\\cmc.data',
                 'test_path': '\\cmc\\cmc.data'})
datasets.append({'name': 'htru_2',
                 'data_train': DatasetsFactory.htru_2,
                 'data_test': DatasetsFactory.htru_2,
                 'train_path': '\\htru_2\\HTRU_2.arff',
                 'test_path': '\\htru_2\\HTRU_2.arff'})
datasets.append({'name': 'data_banknote',
                 'data_train': DatasetsFactory.data_banknote,
                 'data_test': DatasetsFactory.data_banknote,
                 'train_path': '\\banknote_authentication\\data_banknote_authentication.txt',
                 'test_path': '\\banknote_authentication\\data_banknote_authentication.txt'})
datasets.append({'name': 'data_occupancy',
                 'data_train': DatasetsFactory.data_occupancy,
                 'data_test': DatasetsFactory.data_occupancy,
                 'train_path': '\\occupancy_data\\datatraining.txt',
                 'test_path': '\\occupancy_data\\datatest.txt'})

for dataset in datasets:
    best = {'ephoc': 0, 'accurancy': 0, 'train_len': 0, 'test_len': 0, 'time': 0}
    tests = []
    print("\nStarting with " + dataset['name'])
    for ephoc in ephocs_train:
        for train in train_vector:
            to_predict, labels = dataset['data_train'](dataPath + dataset['train_path'], test / 2, test / 2)
            x, y = dataset['data_test'](dataPath + dataset['test_path'], train / 2, train / 2)
            test_len = len(x)
            train_len = len(to_predict)
            start = time.time()
            accurancy = testData(x, y, ephoc, to_predict, labels)
            elapsed = time.time() - start
            tests.append([ephoc, test_len, train_len, accurancy, elapsed])
            if best['accurancy'] < accurancy:
                best['ephoc'] = ephoc
                best['accurancy'] = accurancy
                best['train_len'] = train_len
                best['test_len'] = test_len
                best['time'] = elapsed
    save_results(tests, dataset, best)
    if to_plot:
        plot_data(tests)

    print("Best accurancy: ", best['accurancy'])
    print("ephoc: ", best['ephoc'])
    print("train N.: ", best['train_len'])
