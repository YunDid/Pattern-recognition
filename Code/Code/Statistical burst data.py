import numpy as np
import pandas as pd
import os
def get_Matfile(path):  
    path_list = os.listdir(path)
    #path_list.sort(key=lambda x: int(x.split('V')[0]))
    path_list.sort(key=lambda x: int(x[:-5].split('-')[2]))
    # path_list.sort()      
files = []
    for filename in path_list:
        files.append(os.path.join(path, filename))
    return files

def read_csv(csvfilePath):
    data = pd.read_csv(csvfilePath, header=None)
    data = np.array(data)
    #data = np.round(data, 3)
    #rd, cd = data.shape
    #csvdata = np.reshape(data, cd)
    return data
def mean_data(total_data,active_mean_node_index):
    active_data=total_data[active_mean_node_index]
    mean_active_data=np.mean(active_data)
    return np.round(mean_active_data,3)
path=r'Burst_Data_File_Path'
files=get_Matfile(path)
Mean_Spikes_Num=[]
Network_Spikes=[]
Burst_Num=[]
Bursts_Per_Minute=[]
MBD=[]
MSIB=[]
MISIB=[]
MIBI=[]
total_data=np.zeros((8,5))
for f in range(len(files)):
    print(files[f])
    data=pd.read_excel(files[f])
    #print(data.shape)
    spikes=data['Spikes']
    active_node = np.where(spikes > 0)
    active_node=active_node[0]
    print(active_node)
    print('active_len',len(active_node))
    Mean_Spikes_Num.append(mean_data(spikes,active_node)/600)#spikes/s
    Network_Spikes.append(np.sum(spikes)/600)
    Number_burst=data['Num. Bursts']#Network_Burst(/min)
    Burst_Num.append(np.sum(Number_burst)/10)
    Bursts_per_Minute=data['Bursts Per Minute']#MBR
    Bursts_Per_Minute.append(mean_data(Bursts_per_Minute,active_node))
    Mean_BD=data['Mean Burst Duration']
    MBD.append(mean_data(Mean_BD,active_node))
    Mean_spike_in_burst=data['Mean Spikes in Burst']
    MSIB.append(mean_data(Mean_spike_in_burst,active_node))
    Mean_ISI_in_burst=data['Mean ISI in Burst']
    MISIB.append(mean_data(Mean_ISI_in_burst,active_node))
    Mean_IBI=data['Mean Interburst Interval']
    MIBI.append(mean_data(Mean_IBI,active_node))
total_data[0,:]=Mean_Spikes_Num
total_data[1,:]=Network_Spikes
total_data[2,:]=Burst_Num
total_data[3,:]=Bursts_Per_Minute
total_data[4,:]=MBD
total_data[5,:]=MSIB
total_data[6,:]=MISIB
total_data[7,:]=MIBI
print('MFR',Mean_Spikes_Num)
print('Network spikes',Network_Spikes)
print('Network_Burst/min',Burst_Num)
print('MBR/min',Bursts_Per_Minute)
print('Mean Burst Duration',MBD)
print('Mean Spikes in Burst',MSIB)
print('Mean ISI in Burst',MISIB)
print('Mean Interburst Interval',MIBI)
    # print(np.mean(spikes))
    # print(active_node[0])
total_data=pd.DataFrame(data=total_data)
total_data.to_csv(r'Save_file_name',header=None,index=False)