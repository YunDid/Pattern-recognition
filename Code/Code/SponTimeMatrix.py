import pandas as pd
import scipy.io
import numpy as np
import os



import pandas as pd
import scipy.io
import numpy as np
import os


def main():
        excel_file = pd.read_excel(）
               neuron_names = excel_file['Variables'].values.tolist()
    num_neurons = len(neuron_names)
    output_folder = r'SponMatrixTime File'    
    mat_folder = r'Spon Data File'
    mat_files = os.listdir(mat_folder)
    for mat_file_name in mat_files:
        if mat_file_name.endswith('.mat'):
            mat_file_path = os.path.join(mat_folder, mat_file_name)
            mat_file = scipy.io.loadmat(mat_file_path)
                      result_matrix = np.zeros((num_neurons, 6000))
            for i, name in enumerate(neuron_names):
                if name in mat_file:
                    data = mat_file[name]
                    data_shape = np.shape(data)
                                      if len(data_shape) == 1:  
                        if data_shape[0] <= 6000:
                            result_matrix[i, :data_shape[0]] = data
                        else:
                            result_matrix[i] = data[:6000]
                    elif len(data_shape) == 2:  
                        num_rows, num_cols = data_shape
                        if num_rows * num_cols <= 6000:
                            result_matrix[i, :num_rows * num_cols] = data.flatten()
                        else:
                            result_matrix[i] = data.flatten()[:6000]
            result_df = pd.DataFrame(result_matrix)
            output_excel_file = os.path.join(output_folder, os.path.splitext(mat_file_name)[0] + '.xlsx')
            print(output_excel_file)
            result_df.to_excel(output_excel_file, index=False,header=None)


if __name__ == "__main__":
    main()