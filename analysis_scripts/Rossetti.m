%Code to analyze data from Rossetti experiment


clear all;
close all;

%DATA FORMAT: 
%Time[s] | Line Position | Line Size | Prism Shift | Parietal Line | ...
%Motor Map | Parietal Finger | Leftward Error | Rightward Error | ...
%Add |

mm_PER_PIXEL=2;
LINE_SIZE_IN_PIXELS=40;
LINES=30;  %Number of line sizes shown in the simulation
FOLDER='/home/steven/Dropbox/Research/Paper/data/Run Sep 9 2011, PIXELS=120, NEURONS_PER=40/Rossetti D0.0/';
% FOLDER='/home/sleigh/Dropbox/Research/Paper/data/Run Aug 24 2011, PIXELS=120, NEURONS_PER=40/Rossetti D0.5/';
%FOLDER='/home/sleigh/Dropbox/Research/Paper/data/Run June 25 2011, PIXELS=120, NEURONS_PER=40/Rossetti D0.9/';
% FOLDER='/home/steven/Dropbox/Research/Paper/data/Run July 8 2011, PIXELS=120, NEURONS_PER=40/Rossetti D0.0/';
SAMPLES=size(dir(FOLDER),1)-2; %Number of times the simulation was run

mot_err=zeros(LINES,SAMPLES);
percept_err=zeros(LINES,SAMPLES);
line_positions=zeros(LINES,1);

for i=0:SAMPLES-1,
    path=strcat(FOLDER,int2str(i),'.csv');
    X=load(path);


    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %Make a simple plot for one dimension of simultion data
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % figure ();
    % plot(X(:,1),X(:,3));
    % title('Line Size vs Time');
    % xlabel('Time [s]');;
    % ylabel('Line Size [Pixels?]');


    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %Filter spiking data using these parameters
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %Filter data using linear first order low pass filter
    RC=1;  %RC time constant
    delta_t=0.01;  %sample period
    alpha=delta_t/(RC+delta_t);
    %y=filter(alpha,[1 -(1-alpha)],X(:,5));


    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %Plot all simulation data
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % %Filter all data that is influenced by spiking neurons
%     figure();
%     plot( ...
%         X(:,1),X(:,2), ...
%         X(:,1),X(:,3), ...
%         X(:,1),X(:,4), ...
%         X(:,1),filter(alpha,[1 -(1-alpha)],X(:,5)), ...
%         X(:,1),filter(alpha,[1 -(1-alpha)],X(:,6)), ...
%         X(:,1),filter(alpha,[1 -(1-alpha)],X(:,7)), ...
%         X(:,1),filter(alpha,[1 -(1-alpha)],X(:,8)), ...
%         X(:,1),filter(alpha,[1 -(1-alpha)],X(:,9)), ...
%         X(:,1),filter(alpha,[1 -(1-alpha)],X(:,10)) ...
%         );
%     title('Aggregate Simulation Data');
%     xlabel('Time [s]');
%     legend('Line Position','Line Size','Prism Shift','Parietal Line', ...
%         'Motor Map','Parietal Finger','Leftward Error', ...
%         'Rightward Error','Add');


    
    %low pass filter all simulation data
    filtX=filter(alpha,[1 -(1-alpha)],X);
    %filt_mot_err=filter(alpha,[1 -(1-alpha)],X(:,6));
    
    %Subsample the True Motor Error.  Only keep the sample at the end of a line
    %presentation.  Doing this will help remove transients.
    for j=1:size(X,1),
        if j==size(X,1) || ...  %short circuit for last line presentation
                (X(j,2) ~=X(j+1,2)),  %true when the line has just changed position
            sets=floor(X(j,1)/15)  %an index that changes when a new set of lines is being shown
%             X(j,2)/5+3
            mot_err(5*sets+X(j,2)/5+3,i+1)=filtX(j,6)-X(j,2);
            percept_err(5*sets+X(j,2)/5+3,i+1)=filtX(j,5)-(X(j,2)+X(j,4)); %also take the prism shift into account
            %mot_err(X(j,2)+11,i+1)=filt_mot_err(j);
            %line_positions(X(j,2)+11)=X(j,2);
        end
    end
    
end
%line_positions=repmat([-10,-5,0,5,10],1,6);

figure();
%plot(line_positions,mot_err);
plot(mot_err);
title('Aggregate Motor Error vs Line Position');
xlabel('Phase');
ylabel('Motor Error [Pixles]');
set(gca,'XTick', 1:5:30);
set(gca,'XTickLabel',{'Pre','During','During','Post','Post','Late','End'});

figure();
%errorbar(line_positions,mean(mot_err'),std(mot_err'));
errorbar(1:30,mean(mot_err'),std(mot_err'),'o');
title('Mean Motor Error vs Line Position (Error bars are STD)');
xlabel('Phase');
ylabel('Motor Error [Pixles]');
% set(gca,'XTick',[0:5:30]);
set(gca,'XTick', 1:5:30);
set(gca,'XTickLabel',{'Pre','During','During','Post','Post','Late','End'});


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Load human data
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% .m data format
% data from Rossetti et al. 1998
%Columns: Left|Center|Right
%Rows: Pre;Post;Late
% Numbers are percent of half line size.
% Line size is not reported in paper, but it says the Schenckenberg et al.
% test was used.
% N=6
load('Rossetti_Mean_Patients');
load('Rossetti_SD_Patients');

%Line size: 235 mm
%Errors are reported in mm

load('Danckert_Mean_LB');
load('Danckert_SD_LB');


load('Vallar_Mean_Patients');
load('Vallar_SD_Patients');


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Plot line bisection data in format similar to Rossetti paper
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%error bar line ends don't scale properly, so all data has to be put on one
%plot at once
figure();
hold on;
D = errorbar([-1.1,-0.1,0.9], ...
    mean(Danckert_Mean_LB(:,:),1)./2.35, ...
    sqrt(mean(Danckert_SD_LB(:,:).^2,1)./3)./2.35,':*g');

R = errorbar([-1.05,-0.05,0.95], ...
    Rossetti_Mean_Patients(:,2)./2,Rossetti_SD_Patients(:,2)./2,':xr');

S = errorbar([-1,0,1], ...
    [mean(mot_err(3,:)'); ...
    mean(mot_err(18,:)'); ...
    mean(mot_err(28,:)')]./LINE_SIZE_IN_PIXELS.*100, ...
    [std(mot_err(3,:)'); ...
    std(mot_err(18,:)'); ...
    std(mot_err(28,:)')]./LINE_SIZE_IN_PIXELS.*100,':ob');

% R = errorbar([[-1.15,-1.05,-0.95];[-0.15,-0.05,+0.05];[0.85,0.95,1.05]], ...
%     Rossetti_Mean_Patients(:,:)./2,Rossetti_SD_Patients(:,:)./2,':xr');
% 
% S = errorbar([[-1.1,-1,-0.90];[-0.1,0,+0.1];[0.90,1,1.1]], ...
%     [mean([mot_err(1,:);mot_err(3,:);mot_err(5,:)]'); ...
%     mean([mot_err(16,:);mot_err(18,:);mot_err(20,:)]'); ...
%     mean([mot_err(16,:);mot_err(18,:);mot_err(20,:)]')].*mm_PER_PIXEL.*0.8, ...
%     [std([mot_err(1,:);mot_err(3,:);mot_err(5,:)]'); ...
%     std([mot_err(16,:);mot_err(18,:);mot_err(20,:)]'); ...
%     std([mot_err(16,:);mot_err(18,:);mot_err(20,:)]')].*mm_PER_PIXEL.*0.8,':ob');

set(gca,'XTick',-1:1);
set(gca,'XTickLabel',{'Pre','Post','Late'});
xlabel('Prism Phase');
ylabel('Motor Error [% line size]');
legend([D,R(1),S],'Danckert','Rossetti','Simulation');
% text(-1.25,47.5,'Left','FontSize',12);
% text(-1.15,44,'Center','FontSize',12);
% text(-1.00,40.5,'Right','FontSize',12);
title('Line Bisection Prism Amelioration');
% text(-1.45,80,'Left','FontSize',12)
% text(-1.45,55,'Center','FontSize',12)
% text(-1.35,10,'Right','FontSize',12)
%set(gca,'YTick',[10,55,80]);
%set(gca,'YTickLabel',{'Left','Center','Right'});


% figure()
% errorbar([-0.95,0.05,1.05],mean(Vallar_Mean_Patients,1),mean(Vallar_SD_Patients,1),'xr')
% hold on;
% title('Mean Motor Error vs Line Position (Error bars are SD)(Vallar Patients vs Simulation)');
% xlabel('Line Position');
% ylabel('Motor Error [mm]');
% %legend('Simulation','Humans');
% set(gca,'XTick',-1:1);
% set(gca,'XTickLabel',{'Left','Center','Right'});


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Perform significance tests between post and late samples
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
[h,p] = ttest2(mot_err(18,:),mot_err(28,:));
disp('1 indicates that post and late samples are not likely from the same distribution: ');
disp(h);
disp('p value: ');
disp(p);




%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Process perceptual data as if it were the landmark task
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
figure();
%plot(line_positions,mot_err);
plot(percept_err);
title('Aggregate Perceptual Error vs Line Position');
xlabel('Phase');
ylabel('Motor Error [Pixles]');
set(gca,'XTick', 1:5:30);
set(gca,'XTickLabel',{'Pre','During','During','Post','Post','Late','End'});

figure();
%errorbar(line_positions,mean(mot_err'),std(mot_err'));
errorbar(1:30,mean(percept_err'),std(percept_err'),'o');
title('Mean Perceptual Error vs Line Position (Error bars are STD)');
xlabel('Phase');
ylabel('Motor Error [Pixles]');
% set(gca,'XTick',[0:5:30]);
set(gca,'XTick', 1:5:30);
set(gca,'XTickLabel',{'Pre','During','During','Post','Post','Late','End'});


pre_left=0;
post_left=0;
late_left=0;

for i=1:SAMPLES,
   if (percept_err(3,i)>0),
       pre_left=pre_left+1;  
   end
   
   if (percept_err(18,i)>0),
       post_left=post_left+1;
   end
   
   if (percept_err(28,i)>0),
       late_left=late_left+1;
   end
end

pre_percent=100*pre_left/(SAMPLES);
post_percent=100*post_left/(SAMPLES);
late_percent=100*late_left/(SAMPLES);


%load data from Striemer and Danckerts paper about prism adaptation and
%line bisection and the landmark task.  
%Columns: pre|post|late
%rows are subjects
load('Danckert_Landmark_Patients');
load('Danckert_Landmark_Control');


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Main Landmark Task plots
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
figure();
bar([Danckert_Landmark_Control;pre_percent,post_percent]);
title('Landmark Task Controls');
legend('Pre','Post');
set(gca,'XTickLabel',{'1','2','3','4','5','6','7','8','SIM'})
ylabel('Percentage of left responses');
xlabel('Subject');

figure();
bar([Danckert_Landmark_Patients;pre_percent,post_percent,late_percent]);
title('Landmark Task Neglect');
legend('Pre','Post','Late');
set(gca,'XTickLabel',{'NS','SQ','RR','SIM'})
ylabel('Percentage of left responses');
xlabel('Patient');





%end