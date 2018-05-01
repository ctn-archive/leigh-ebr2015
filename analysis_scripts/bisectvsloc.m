%Code to analyze data from bisecvsloc experiment


clear all;
close all;

%DATA FORMAT: 
%Time[s] | Line Position | Line Size | Prism Shift | Parietal Line | ...
%Motor Map | Parietal Finger | Leftward Error | Rightward Error | ...
%Add |

LINES=5;  %Number of line sizes shown in the simulation
mm_PER_PIXEL=2;
FOLDER='/home/sleigh/Dropbox/Research/Paper/data/Run June 25 2011, PIXELS=120, NEURONS_PER=40/bisectvsloc D0.5/';
SAMPLES=size(dir(FOLDER),1)-2; %Number of times the simulation was run

mot_err=zeros(LINES,SAMPLES);
percept_err=zeros(LINES,SAMPLES);
line_positions=zeros(LINES,1);

for i=0:SAMPLES-1,
%     path=strcat('/home/sleigh/Dropbox/Research/Paper/data/Run June 8 2011, PIXELS=120, NEURONS_PER=40/bisectvsloc/',int2str(i),'.csv');
    path=strcat(FOLDER,int2str(i),'.csv');
    X=load(path);
    %X=load('/home/sleigh/Dropbox/Research/Paper/data/Run May 13 2011/Halligan/0.csv');



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
    RC=0.5;  %RC time constant
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
    %filt_percept_err=filter(alpha,[1 -(1-alpha)],X(:,7));
    
    %Subsample the True Motor Error.  Only keep the sample at the end of a line
    %presentation.  Doing this will help remove transients.
    for j=1:size(X,1),
        if X(j,1)>15 && ...  %lines are shown 2 times.  Gather only samples from 2nd time.
                (j==size(X,1) || ...  %short circuit for last line presentation
                (X(j,2) ~=X(j+1,2))),  %true when the line has just changed position
            mot_err(X(j,2)/5+3,i+1)=filtX(j,6)-X(j,2);
            percept_err(X(j,2)/5+3,i+1)=filtX(j,5)-(X(j,2)+X(j,4)); %also take the prism shift into account
            line_positions(X(j,2)/5+3)=X(j,2);
        end
    end
    
end


figure();
plot(line_positions,mot_err);
title('Aggregate Motor Error vs Line Position');
xlabel('Line Position [Pixles]');
ylabel('Motor Error [Pixles]');

figure();
errorbar(line_positions,mean(mot_err'),std(mot_err'),'x');
title('Mean Motor Error vs Line Position (Error bars are SD)');
xlabel('Line Position [Pixles]');
ylabel('Motor Error [Pixles]');

figure();
errorbar(line_positions,mean(percept_err'),std(percept_err'),'x');
title('Mean Perceptual Error vs Line Size (Error bars are SD)');
xlabel('Line Size [Pixels]');
ylabel('Perceptual Error [Pixles]');



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Load human data
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%% .m data format
%Data from Vallar et al. 2000
%column: line locations: left|center|right
%rows: line sizes: 8cm;16cm;24cm
%Line positions for non-centered lines were such that a line endpoint was
%centered on the subject's mid-saggital plane of the trunk.
%mean and SD are in mm.  +ve is right, -ve is left
%6 controls and 6 patients
%All data is of only normal lines with no illusions
load('Vallar_Mean_Control');
load('Vallar_Mean_Patients');
load('Vallar_SD_Control');
load('Vallar_SD_Patients');

Vallar_Positions=[-40,0,40;-80,0,80;-120,0,120];  

figure()
errorbar(Vallar_Positions(1,:),Vallar_Mean_Control(1,:),Vallar_SD_Control(1,:),'r')
hold on;
errorbar(Vallar_Positions(2,:),Vallar_Mean_Control(2,:),Vallar_SD_Control(2,:),'g')
errorbar(Vallar_Positions(3,:),Vallar_Mean_Control(3,:),Vallar_SD_Control(3,:),'b')
title('Vallar Mean Motor Error vs Line Position (Error bars are SD)');
xlabel('Line Position [mm]');
ylabel('Motor Error [mm]');
legend('80mm line','160mm line','240mm line');

figure()
errorbar(line_positions.*mm_PER_PIXEL,mean(mot_err').*mm_PER_PIXEL,std(mot_err').*mm_PER_PIXEL,'x');
hold on;
errorbar(Vallar_Positions(1,:),Vallar_Mean_Control(1,:),Vallar_SD_Control(1,:),'xr')
title('Mean Motor Error vs Line Position (Error bars are SD)');
xlabel('Line Position [mm]');
ylabel('Motor Error [mm]');
legend('Vallar 80mm Control','Simulation 80mm Control');


figure()
errorbar([-1.05;-0.05;0.95],mean([mot_err(1,:);mot_err(3,:);mot_err(5,:)]').*mm_PER_PIXEL,std([mot_err(1,:);mot_err(3,:);mot_err(5,:)]').*mm_PER_PIXEL,'o');
hold on;
errorbar([-0.95,0.05,1.05],mean(Vallar_Mean_Control,1),mean(Vallar_SD_Control,1),'xr')

title('Healthy Controls');
xlabel('Line Position');
ylabel('Mean Motor Error [mm]');
legend('Simulation','Human');
set(gca,'XTick',-1:1)
set(gca,'XTickLabel',{'Left','Center','Right'})
axis([-1.5 1.5 -30 90])



figure()
errorbar([-1.05;-0.05;0.95],mean([mot_err(1,:);mot_err(3,:);mot_err(5,:)]').*mm_PER_PIXEL,std([mot_err(1,:);mot_err(3,:);mot_err(5,:)]').*mm_PER_PIXEL,'o');
hold on;
errorbar([-0.95,0.05,1.05],mean(Vallar_Mean_Patients,1),mean(Vallar_SD_Patients,1),'xr')

title('Neglect Patients');
xlabel('Line Position');
ylabel('Mean Motor Error [mm]');
legend('Simulation','Human');
set(gca,'XTick',-1:1);
set(gca,'XTickLabel',{'Left','Center','Right'});
axis([-1.5 1.5 -30 90])









%end