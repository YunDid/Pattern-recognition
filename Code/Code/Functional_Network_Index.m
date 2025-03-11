clc
clear
charpath_array=[]
G_eff=[]
C_array=[]
S_array=[]
Density_aray=[]
E_array=[]
g_e_ARRAY=[]
l_e_array=[]
modulari_array=[]
maindir='Functional Neural Network File Path';
subdir=dir(fullfile(maindir,'*.csv'));
fileNames={subdir.name};

bin_FM_maindir='';
bin_subdir=dir(fullfile(bin_FM_maindir,'*.csv'))
bin_fileNames={bin_subdir.name};

for i=1:length(fileNames)
    path=strcat(maindir,fileNames(i));
    data=csvread(path{1})
    shape=size(data)
    if shape(1)==65
        data=data(2:end,2:end)
    else
        data=data
    end
    bin_path=strcat(bin_FM_maindir,bin_fileNames(i));
    bin_FM_data=csvread(bin_path{1})
    
[lambda] = charpath(bin_FM_data,0,1)
charpath_array=[charpath_array,lambda]
C=clustering_coef_bu(bin_FM_data)
C_array=[C_array,C]

[smallwdness,C,L] = small_world(bin_FM_data)
S_array=[S_array,smallwdness]

[kden,N,K] = density_und(data)
Density_aray=[Density_aray,kden]

E = efficiency_wei(data, 0)
E_array=[E_array,E]

[Ci,Q]=modularity_und(data,1)
modulari_array=[modulari_array,Q]%max modularity

bin_E=efficiency_bin(bin_FM_data,0)
g_e_ARRAY=[g_e_ARRAY,bin_E]

bin_L_E=efficiency_bin(bin_FM_data,1)
l_e_array=[l_e_array,bin_L_E]
end
mean_charpath_array=mean(charpath_array)
mean_C_array=mean(C_array)
mean_C_array=mean(mean_C_array)
mean_S_array=mean(S_array)
mean_Density_aray=mean(Density_aray)
mean_E_array=mean(E_array)
mean_g_e_ARRAY=mean(g_e_ARRAY)
mean_L_array=mean(mean(l_e_array))
mean_max_modularity=mean(modulari_array)