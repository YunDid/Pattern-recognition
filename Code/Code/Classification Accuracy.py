from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, precision_score, recall_score, accuracy_score
import pandas as pd
import os
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.neighbors import NearestCentroid
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.cluster import kmeans_plusplus
from sklearn.metrics import classification_report, confusion_matrix, precision_score, recall_score, accuracy_score
from sklearn.ensemble import RandomForestClassifier

def get_file(path):
    path_list = os.listdir(path)
    #path_list.sort(key=lambda x: int(x.split('-')[0]))
    path_list.sort()
    files = []
    for filename in path_list:
        files.append(os.path.join(path, filename))
    return files
def get_CSVfile(path):
    path_list = os.listdir(path)
    path_list.sort(key=lambda x: int(x.split('-')[0]))
    #path_list.sort()
    files = []
    for filename in path_list:
        files.append(os.path.join(path, filename))
    return files

def read_csv(path):
    data = pd.read_csv(path, header=None)
    data = np.array(data)
    return data
import numpy as np
path_csv = r'StimData‘
csv_files = get_file(path_csv)
print(csv_files)
for cf in range(len(csv_files)):
    csv_name=csv_files[cf]
    print(csv_name)
    csv_name=csv_name.split('\\')[0]#5
    files = get_CSVfile(csv_files[cf])
    print(files)
    Y_TEST_SCORE = []
    dataL=read_csv(files[0])
    print(dataL[0].shape)
    row=dataL[0].shape
    print(row[0])
    traingData = np.zeros((1, row[0]))  #
    testingData = np.zeros((1, row[0]))  #
    column_num = dataL.shape[1]
    dataX=read_csv(files[1])
    #column_num = dataX.shape[1]
    dataL2=read_csv(files[2])
    dataS=read_csv(files[3])
    dataL3 = read_csv(files[4])
    dataC = read_csv(files[5])


    for t in range(5):  # 5
        totaltrain = np.zeros(dataX.shape[1])
        totaltest = np.zeros(dataX.shape[1])
        traindataL = dataL[80 * t:80 * (t + 1), :]
        #print(traindataL.shape)
        traindataX = dataX[80 * t:80 * (t + 1), :]
        traindataL2=dataL2[80 * t:80 * (t + 1), :]
        traindataS=dataS[80 * t:80 * (t + 1), :]
        traindataC = dataC[80 * t:80 * (t + 1), :]
        traindataL3 = dataL3[80 * t:80 * (t + 1), :]

        # #print(traindataX.shape)
        totaltrain = np.row_stack((totaltrain, traindataL[:60, :]))  # 60
        totaltrain = np.row_stack((totaltrain, traindataX[:60, :]))
        totaltrain = np.row_stack((totaltrain, traindataL2[:60, :]))
        totaltrain = np.row_stack((totaltrain, traindataS[:60, :]))
        totaltrain = np.row_stack((totaltrain, traindataC[:60, :]))
        totaltrain = np.row_stack((totaltrain, traindataL3[:60, :]))


        totaltest = np.row_stack((totaltest, traindataL[60:, :]))
        totaltest = np.row_stack((totaltest, traindataX[60:, :]))
        totaltest = np.row_stack((totaltest, traindataL2[60:, :]))
        totaltest = np.row_stack((totaltest, traindataS[60:, :]))
        totaltest = np.row_stack((totaltest, traindataC[60:, :]))
        totaltest = np.row_stack((totaltest, traindataL3[60:, :]))

        clf=svm.SVC(kernel='rbf', C=1.0, gamma='auto')
        #clf = RandomForestClassifier()
        #clf=NearestCentroid()
        #clf=LinearDiscriminantAnalysis()
        r = totaltrain.shape
        totaltrain = totaltrain[1:, :]
        #print(totaltrain.shape)
        totaltest = totaltest[1:, :]
        #print(totaltest.shape)
        x_train = totaltrain[:, :column_num - 1]
        y_train = totaltrain[:, column_num - 1]
        x_test = totaltest[:, :column_num - 1]
        y_test = totaltest[:, column_num - 1]
        clf.fit(x_train, y_train.ravel())
        # print("trainingprediction:%.3f" % (clf.score(x_train, y_train)))
        # print("testOdataprediction:%.3f" % (clf.score(x_test, y_test)))

        y_pred = clf.predict(x_test)
        Y_TEST_SCORE.append(np.round(accuracy_score(y_test, y_pred),3))
    print(Y_TEST_SCORE)
    print(np.std(Y_TEST_SCORE))
    print('average_accuracy', np.round(sum(Y_TEST_SCORE) /5,3))
