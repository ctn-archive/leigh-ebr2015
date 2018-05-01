%Code to analyze data from adapt experiment


clear all;
close all;

%DATA FORMAT: 
%Time[s] | Line Position | Line Size | Prism Shift | Parietal Line | ...
%Motor Map | Parietal Finger | Leftward Error | Rightward Error | ...
%Add |

mm_PER_PIXEL=2;
FOLDER='/home/steven/Dropbox/Research/Paper/data/Run Jan 29 2012, PIXELS=120, NEURONS_PER=40/Adapt D0.9/';
SAMPLES=size(dir(FOLDER),1)-2; %Number of times the simulation was run

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
    RC=10;  %RC time constant
    delta_t=0.01;  %sample period
    alpha=delta_t/(RC+delta_t);
    %y=filter(alpha,[1 -(1-alpha)],X(:,5));


    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %Plot all simulation data
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % %Filter all data that is influenced by spiking neurons
    figure();
    plot( ...
        X(:,1),X(:,2), ...
        X(:,1),X(:,3), ...
        X(:,1),X(:,4), ...
        X(:,1),filter(alpha,[1 -(1-alpha)],X(:,5)), ...
        X(:,1),filter(alpha,[1 -(1-alpha)],X(:,6)), ...
        X(:,1),filter(alpha,[1 -(1-alpha)],X(:,7)), ...
        X(:,1),filter(alpha,[1 -(1-alpha)],X(:,8)), ...
        X(:,1),filter(alpha,[1 -(1-alpha)],X(:,9)), ...
        X(:,1),filter(alpha,[1 -(1-alpha)],X(:,10)) ...
        );
    title('Aggregate Simulation Data');
    xlabel('Time [s]');
    legend('Line Position','Line Size','Prism Shift','Parietal Line', ...
        'Motor Map','Parietal Finger','Leftward Error', ...
        'Rightward Error','Add');
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %Plot formatted for paper
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%    
    figure();
    plot(X(:,1),X(:,4).*mm_PER_PIXEL,'--r');
    hold on;
    plot(X(:,1),filter(alpha,[1 -(1-alpha)],X(:,6)).*mm_PER_PIXEL);
    title('Neglect Prism Adaptation');
    xlabel('Time [s]');
    ylabel('Azimuthal Displacement [mm]');
    legend('Prism Shift','Finger Position');


   
end

% figure();
% %plot(line_positions,mot_err);
% plot(mot_err);
% title('Aggregate Motor Error vs Line Position');
% xlabel('Line Position [Pixles]');
% ylabel('Motor Error [Pixles]');
% 
% figure();
% %errorbar(line_positions,mean(mot_err'),std(mot_err'));
% errorbar(mean(mot_err'),std(mot_err'));
% title('Mean Motor Error vs Line Position (Error bars are STD)');
% xlabel('Line Position [Pixles]');
% ylabel('Motor Error [Pixles]');



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Load human data
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% .m data format
% data unpublished from Danckert
% Numbers are mm for line bisection (LB), or % of Left responses for the
% landmark task.
% Line size?
% columns are pre|post|late prism exposure
% rows are for patients NS;SQ;RR
load('Danckert_Mean_LB');
load('Danckert_SD_LB');
load('Danckert_Landmark');











%end