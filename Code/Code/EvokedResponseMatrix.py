import os
from scipy.io import loadmat
import pandas as pd
import numpy as np
import scipy.io
import scipy.io as sio
def read_SIOmat(matfiles):
    data = sio.loadmat(matfiles)
    datava = list(data.values())[3]
    datava=np.array(datava)
    return datava

def process_and_save_matrix(excel_file_path, stimulus_time_file_path, data_file_path):
   
    union_variable_df = pd.read_excel(excel_file_path, sheet_name="All_Channels")
    all_variable_names = union_variable_df["Variables"].tolist()
    print('all_variable_names',all_variable_names)
    print(len(all_variable_names))

    stim_mat_data = read_SIOmat(stimulus_time_file_path)
    stimTimeData = np.round(stim_mat_data, 3)
    stimulus_times = stimTimeData[:,0]
    print(len(stimTimeData))

   
    data = loadmat(data_file_path)
    print(data)

    result_matrix = np.zeros((len(stimulus_times), len(all_variable_names)))
 
    stimTimeMatrix=np.zeros((len(all_variable_names),6000))

    for stim_idx, stim_time in enumerate(stimulus_times):
        for var_idx, var_name in enumerate(all_variable_names):
            if var_name in data:
                var_data = data[var_name]
                var_data=np.round(var_data,3)
                              valid_count = np.sum((var_data >= stim_time + 0.01) & (var_data <= stim_time + 0.05))
                result_matrix[stim_idx, var_idx] = valid_count
                
                #length_spike_50 = var_data((var_data >=stim_time + 0.01) & (var_data <= stim_time + 0.05))
                length_spike_50 = var_data[(var_data >= stim_time + 0.01) & (var_data <= stim_time + 0.05)]
                print(length_spike_50)  


                inser_length = len(length_spike_50)

                inser_index = np.where(stimTimeMatrix[var_idx, :] > 0)
                inser_index = np.array(inser_index)
                inser_index = len(inser_index[0])

                if inser_length == 0:
                    continue
                else:
                    if inser_index == 0:
                        stimTimeMatrix[var_idx, :inser_length] = length_spike_50
                    else:
                        stimTimeMatrix[var_idx, inser_index:inser_index + inser_length] = length_spike_50



            else:
                continue
    return result_matrix,stimTimeMatrix


excel_file_path = r"stim_spon_combine_neurons_variables File Path"
stimulus_time_file_path = r""
data_file_path = r"SSD"
spike_data=read_SIOmat(data_file_path)
print('spike_data',spike_data)
result_matrix,stimTimeMatrix = process_and_save_matrix(excel_file_path, stimulus_time_file_path, data_file_path)
result_matrix=pd.DataFrame(data=result_matrix)
print(result_matrix.shape)
#result_matrix.to_csv(file_name,header=None,index=False)
stimTimeMatrix=pd.DataFrame(data=stimTimeMatrix)
stimTimeMatrix.to_csv(r'file_name',header=None,index=False)
