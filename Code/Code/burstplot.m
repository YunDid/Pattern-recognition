clc
clear 
close all
maindir='Mat_File_Path';
savedir='BrustPicture_File_Path';
subdir=dir(fullfile(maindir,'*.mat'));
fileNames={subdir.name};
for i=1:length(fileNames)
    % yyaxis left
    path=strcat(maindir,fileNames(i));
    data=load(path{1,1});
    namess=fieldnames(data);
    d=0;
    spike=[];

    for r=1:length(namess)
            names=namess{r,1};
            d=d+1;
            dataa=extractfield(data,names);
            dataa=dataa(dataa>0 & dataa<20)
            spike=[spike,dataa];
            for f=1:length(dataa)
                plot([dataa(f),dataa(f)],[d-1,d-0.1],'LineStyle','-','Marker','none','Color',[0,0,0],'linewidth',1)%[98/256,187/256,237/256]
                hold on
            end
    end
        axis([0 60,0 32])
    xlim([0,20])
    ylim([0,length(namess)])
    set(gca,'ycolor',[0,0,0])%[98/256,187/256,237/256]
    xlabel('Time(s)')
    ylabel('Electrode')
        set(gca,'xtick',[],'ytick',[])
        set(gca,'Visible','off')
    fr=[];
    for h=1:100
        t1=0.1*(h-1);
        t2=t1+0.1;
        a=length(find(spike>t1 & spike<=t2));
        fr(h)=a;
    end

    fr=fr/0.1/1000;
    b=max(fr);
    fr1=smoothdata(fr,'gaussian',8);
    x=(0.1:0.1:10);
    % yyaxis right

    plot(x,fr1,'Color',[253/256,65/256,54/256],'linewidth',2)
    ylim([0,4])
    ylabel('Pop.firing rate(kHz)')
    % set(gca,'ycolor',[253/256,65/256,54/256])
    set(gca,'Visible','off')
    savepath= strcat(savedir,fileNames(i));
    savepath=erase(savepath,'.mat');
    print(gcf,savepath{1,1},'-r600','-djpeg')
    close
end
