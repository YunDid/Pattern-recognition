clc
clear
filename1=ls('D:\219顺序刺激\mat\1.17cell1\stimFM\1')
filename=cellstr(filename1);                       %把细胞数组转化为字符串
filename(1:2)=[];    
filename=sort_nat(filename)
SaArray=zeros(1,6)
LengthArray=zeros(1,6)
CluArray=zeros(1,6)
DensityArray=zeros(1,6)
for fileth=1:length(filename)
    Name=filename{fileth,1}
    MatrixData=csvread(['D:\219顺序刺激\mat\1.17cell1\stimFM\1','\\',Name]);%得到struct类型的数据
    [kden] = density_und(MatrixData)%计算密度
    DensityArray(1,fileth)=kden
    [RandomNetwork]=randmio_und(MatrixData, 10)%生成一个随机网络
    meanCa=clustering_coef_wu(MatrixData)%初始网络的聚类系数
    CluArray(1,fileth)=meanCa
    meanRa=clustering_coef_wu(RandomNetwork)%随机网络的聚类系数
    La= charpath(MatrixData,0,1)%初始网络的特征路径长度
    LengthArray(1,fileth)=La
    LRa=charpath(RandomNetwork,0,1)%随机网络的特征路径长度
    Sa=(meanCa*LRa)/(meanRa*La)
    SaArray(1,fileth)=Sa
end
 