import pandas as pd
import numpy as np
import os
import math
import multiprocessing
from functools import partial
from time import time

def get_sum(num1, num2, array):
    return np.sum((array >= num1) & (array <= num2))

def get_Matfile(path):
    path_list = os.listdir(path)
    files = []
    for filename in path_list:
        files.append(os.path.join(path, filename))
    return files

def Cal_allNeuronCrossMartix(response_Data, two, neuron_num):
    refData = two[:6000]
    refData = np.array(refData)
    refNum = int(two[-1])
    print('ref', refNum)
    ref = refData[(0 < refData) & (refData <= 600)]
    singlecorr = np.zeros(neuron_num)
    if len(ref) == 0:
        return singlecorr
    for t in range(refNum):
        taget = response_Data[t, :]
        taget = taget[(0 < taget) & (taget <= 600)]
        if len(taget) == 0:
            singlecorr[t] = 0
        else:
            rbegin = ref - 0.05
            bleft = rbegin[:, np.newaxis] + np.arange(50) * 0.002
            bright = rbegin[:, np.newaxis] + (np.arange(50) + 1) * 0.002
            refspiketrain = np.array([get_sum(bleft[i, j], bright[i, j], taget) for i in range(len(ref)) for j in range(50)]).reshape(len(ref), 50)
            a = np.sum(refspiketrain, axis=0)
            c = math.sqrt(len(ref) * len(taget))
            a = a / c
            singlecorr[t] = np.max(a)
            print('ref-taget-correlation', refNum, t, np.max(a))
    singlecorr[refNum:] = -1
    print(singlecorr)
    return singlecorr

def Cal_FM(original_data, neuron_num):
    maxvalueTrain = original_data[:, :neuron_num]
    maxvalueTrain[maxvalueTrain == -1] = 0
    np.fill_diagonal(maxvalueTrain, 0)
    maxvalueTrain = maxvalueTrain.T + maxvalueTrain
    T1CM_Matrix = maxvalueTrain.copy()
    RM_Matrix = maxvalueTrain.copy()
    arr_mean = np.mean(maxvalueTrain)
    arr_std = np.std(maxvalueTrain)
    th1 = arr_mean + 1 * arr_std
    T1CM_Matrix[T1CM_Matrix <= th1] = 0
    RM_Matrix[RM_Matrix > th1] = 0
    TM = np.zeros((neuron_num, neuron_num))
    for r in range(neuron_num):
        rowValue = RM_Matrix[r, :]
        for c in range(neuron_num):
            colValue = np.delete(rowValue, c)
            non_colValue = colValue[colValue.nonzero()]
            if len(non_colValue) > 0:
                Mean = np.mean(non_colValue)
                SD = np.std(non_colValue)
                th = Mean + SD
                TM[r, c] = th
    T2CM = np.where(RM_Matrix >= TM, RM_Matrix, 0)
    FM = T1CM_Matrix + T2CM
    if FM.shape[0] == neuron_num + 1:
        data = FM[1:, 1:]
    else:
        data = FM
    new_data = np.maximum(data, data.T)
    return new_data

def main(dataPath):
    response_matrix = pd.read_excel(dataPath, header=None)
    response_matrix = np.array(response_matrix)
    neuron_num = response_matrix.shape[0]  
    coeffMatrix = np.zeros(neuron_num)
    num = np.array(range(neuron_num))
    itArr = np.column_stack((response_matrix, num))
    iterable = [tuple(row) for row in itArr]
    num_cores = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(num_cores)
    func = partial(Cal_allNeuronCrossMartix, response_matrix, neuron_num=neuron_num)
    everowCoeff = pool.map(func, iterable)
    coeffMatrix = np.vstack(everowCoeff)
    return coeffMatrix

if __name__ == "__main__":
    begin_time = time()
    FilePath = r'\SponMatrix File Path'
    savePath = r' '
    FileName = get_Matfile(FilePath)
    print(FileName)
    for f in range(len(FileName)):
        each_file_name = FileName[f]
        name = os.path.basename(each_file_name)
        name = name.replace('xlsx', 'csv')
        print(name)
        coeffMatrix = main(FileName[f])
        neuron_num = coeffMatrix.shape[0]
        # coeffMatrix = Cal_FM(coeffMatrix, neuron_num)
        coeffMatrix = pd.DataFrame(data=coeffMatrix)
        coeffMatrix.to_csv(savePath + '\\' + name, index=False, header=None)
    end_time = time()
    run_time = end_time - begin_time
    print( run_time)