%Code to analyze data from Halligan's experiment


clear all;
close all;

%DATA FORMAT: 
%Time[s] | Line Position | Line Size | Prism Shift | Parietal Line | ...
%Motor Map | Parietal Finger | Leftward Error | Rightward Error | ...
%Add |

mm_PER_PIXEL=2;
LINES=10;  %Number of line sizes shown in the simulation
% FOLDER='/home/sleigh/Dropbox/Research/Paper/data/Run June 17 2011, PIXELS=120, NEURONS_PER=40/Halligan D0.0/';
FOLDER='/home/steven/Dropbox/Research/Paper/data/Run Sep 9 2011, PIXELS=120, NEURONS_PER=40/Halligan D0.9/';
        
SAMPLES=size(dir(FOLDER),1)-2; %Number of times the simulation was run

mot_err=zeros(LINES,SAMPLES);
percept_err=zeros(LINES,SAMPLES);
line_size=zeros(LINES,1);

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
    %RC=1;  %RC time constant
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
%     filt_mot_err=filter(alpha,[1 -(1-alpha)],X(:,6));
%     filt_percept_err=filter(alpha,[1 -(1-alpha)],X(:,7));
    
    %Subsample the True Motor Error.  Only keep the sample at the end of a line
    %presentation.  Doing this will help remove transients.
    for j=1:size(X,1),
        if j==size(X,1) || X(j,3)~=X(j+1,3),  %true when the line has just changed size
%             mot_err(X(j,3),i+1)=filt_mot_err(j);
%             percept_err(X(j,3),i+1)=filt_percept_err(j);
%             line_size(X(j,3))=X(j,3).*2;
            
            mot_err((X(j,3)-1)/13+1,i+1)=filtX(j,6)-X(j,2);
            percept_err((X(j,3)-1)/13+1,i+1)=filtX(j,5)-(X(j,2)+X(j,4)); %also take the prism shift into account
            line_size((X(j,3)-1)/13+1)=X(j,3);
        end
    end
    i
end


figure();
plot(line_size,mot_err);
title('Aggregate Motor Error vs Line Size');
xlabel('Line Size [Pixels]');
ylabel('Motor Error [Pixles]');

figure();
errorbar(line_size,mean(mot_err'),std(mot_err'),'x');
title('Mean Motor Error vs Line Size (Error bars are SD)');
xlabel('Line Size [Pixels]');
ylabel('Motor Error [Pixles]');

figure();
errorbar(line_size,mean(percept_err'),std(percept_err'),'x');
title('Mean Perceptual Error vs Line Size (Error bars are SD)');
xlabel('Line Size [Pixels]');
ylabel('Perceptual Error [Pixles]');



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Data from Halligan and Marshall 1993
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Only interested in horizontal line bisection for controls and patients

%Load .mat files with data from Halligan's paper
load('Halligan_Mean_Males.mat');
load('Halligan_SD_Males.mat');
load('Halligan_Mean_Females.mat');
load('Halligan_SD_Females.mat');
load('Halligan_Mean_Patients.mat');
load('Halligan_SD_Patients.mat');

%File format:
%Rows are line sizes in mm.  Row 1 is 25mm, Row 11 is 279mm.
%Columns are subjects

%Line sizes from Halligan's experiments in mm
halligan_lines=[25 51 77 102 127 152 178 203 228 254 279];

%Patient initials from left column to right
halligan_patients={'FD' 'DF' 'MN' 'CC' 'BS' 'PP' 'TB' 'EF' 'TR' 'TM'};

%halligan_mean_control=mean([mean(Halligan_Mean_Males,2) , mean(Halligan_Mean_Females,2)],2);

halligan_group_mean_control=[.06 .12 .33 .42 .29 -.01 .08 -.31 .3 -.78 -1.19];  %Taken from table 7
halligan_group_SD_control=[.8 1.3 2 2.8 2.8 3.5 3.6 4.4 4.5 4.8 5];  %Taken from table 7
halligan_group_mean_patients=mean(Halligan_Mean_Patients,2);

%Calculation of the group SD is somewhat complicated given only mean and SD
%of each individual.  The resulting formula looks very similar to the
%parallel axis theorem.
%10 samples per patient
%10 patients
delta=Halligan_Mean_Patients-repmat(halligan_group_mean_patients,1,10);
%sum(9*Halligan_SD_Patients.^2 +10*delta.^2,2)
halligan_group_SD_patients=sqrt((sum(9*Halligan_SD_Patients.^2 +10*delta.^2,2))/(99));


% figure();
% plot(halligan_lines,halligan_group_mean_control);
% title('Halligan Control vs Line Size');
% xlabel('Line Size [mm]');
% ylabel('Motor Error [mm]');

figure();
plot(halligan_lines,[(Halligan_Mean_Males) (Halligan_Mean_Females)]);
title('Halligan Control Aggregate Motor Error vs Line Size');
xlabel('Line Size [mm]');
ylabel('Motor Error [mm]');

figure();
errorbar(halligan_lines,halligan_group_mean_control,halligan_group_SD_control,'xr');
title('Halligan Control Motor Error vs Line Size (Error bars are SD)');
xlabel('Line Size [mm]');
ylabel('Motor Error [mm]');

figure();
plot(halligan_lines,Halligan_Mean_Patients);
title('Halligan Patients Aggregate Motor Error vs Line Size');
xlabel('Line Size [mm]');
ylabel('Motor Error [mm]');

figure();
errorbar(halligan_lines,halligan_group_mean_patients,halligan_group_SD_patients,'xr');
title('Halligan Patients Motor Error vs Line Size (Error bars are SD)');
xlabel('Line Size [mm]');
ylabel('Motor Error [mm]');



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Compare simulation data with Halligan's data
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
figure();
errorbar(line_size.*mm_PER_PIXEL,mean(mot_err').*mm_PER_PIXEL,std(mot_err').*mm_PER_PIXEL,'o');
hold on;
errorbar(halligan_lines,halligan_group_mean_control,halligan_group_SD_control,'xr');
axis([20 250 -30 90])
title('Healthy Controls');
xlabel('Line Size [mm]');
ylabel('Mean Motor Error [mm]');
legend('Simulation','Human');

figure();
errorbar(line_size.*mm_PER_PIXEL,mean(mot_err').*mm_PER_PIXEL,std(mot_err').*mm_PER_PIXEL,'o');
hold on;
errorbar(halligan_lines,halligan_group_mean_patients,halligan_group_SD_patients,'xr');
axis([20 250 -30 90])
title('Neglect Patients');
xlabel('Line Size [mm]');
ylabel('Mean Motor Error [mm]');
legend('Simulation','Human');








%end