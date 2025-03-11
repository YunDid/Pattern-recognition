function [d] = Distla(M)
%M矩阵为二值且无连接关系为Inf,对角线为0
t=1
shape=size(M)
r=shape(1)
c=shape(2)
for i=1:r
    for j=1:c
        if M(i,j)==1
           s(t)=i
           k(t)=j
           t=t+1
        end
    end
end
G = graph(s,k);
d = distances(G)
% for n=1:length(s)
%     if ismember(n,s)==0
%         c=size(d)%求矩阵行列数
%         d(1:c(1),n)=zeros([c(1),1])%在第n列添加同等行数的0
%         d(n,1:c(2)+1)=zeros([1,c(2)+1])%在第n行加多于列数加1的0
%     end
% end
        
