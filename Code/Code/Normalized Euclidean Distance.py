import numpy as np
import pandas as pd
import math
import os
def get_stim_CSVfile(path):  # 创建一个空列表
    path_list = os.listdir(path)
    path_list.sort(key=lambda x: int(x.split('-')[0]))
    #path_list.sort()  # 对读取的路径进行排序
    files = []
    for filename in path_list:
        files.append(os.path.join(path, filename))
    return files
def read_csv(path):
    data = pd.read_csv(path, header=None)
    data = np.array(data)
    if data.shape[0]==65:
        data=data[1:,1:]
    else:
        data=data
    return data
# path=r'DiffFMDidstance_File'
# files=get_stim_CSVfile(path)
# for  f in range(len(files)):
#      data=read_csv(files[f])
#      name=os.path.basename(files[f])
#      print(name)
#      max_num=np.max(data)
#      non_zero_index=np.where(data!=0)
#      non_zero_value=data[non_zero_index]
#      min_num=np.min(non_zero_value)
#      print(min_num)
#      new_data=(data-min_num)/(max_num-min_num)
#      row, col = np.diag_indices_from(new_data)
#      new_data[row, col] = 0
#      #print(np.mean(new_data) / 2)
#      mean_val=np.sum(new_data)/30/2
#      print('mean_val',mean_val)
#      print(new_data)
#      new_data=pd.DataFrame(data=new_data)
#      new_data.to_csv(r'diff_normalized'+'\\'+name,header=None,index=False)

new_data=np.zeros((1,6))
path1=r'DiffFMDidstance_first_day'
data1=pd.read_csv(path1,header=None)
data1=np.array(data1)
path2=r'DiffFMDidstance_Second_day'
data2=pd.read_csv(path2,header=None)
data2=np.array(data2)
path3=r'DiffFMDidstance_Third_day'
data3=pd.read_csv(path3,header=None)
data3=np.array(data3)
new_data=np.row_stack((new_data,data1))
new_data=np.row_stack((new_data,data2))
new_data=np.row_stack((new_data,data3))
new_data=new_data[1:,:]
non_zero_index=np.where(new_data!=0)
non_zero_value=new_data[non_zero_index]
min_num=np.min(non_zero_value)
new_data=(new_data-min_num)/(np.max(new_data)-min_num)
for i in range(3):
    row_data=new_data[i*6:(i+1)*6,:]
    print(row_data.shape)
    row, col = np.diag_indices_from(row_data)
    row_data[row, col] = 0
    mean_val=np.sum(row_data)/30/2
    print(mean_val)
new_data=pd.DataFrame(data=new_data)
new_data.to_csv(r'Saved_normalized_data.csv',header=None,index=False)