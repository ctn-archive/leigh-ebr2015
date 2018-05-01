%Code to analyze data from Halligan's experiment


clear all;
close all;

%DATA FORMAT: 
%Time[s] | Line Position | Line Size | Prism Shift | Parietal Finger | ...
%True Motor Error | True Perceptual Error | Leftward Error | ...
%Rightward Error | Add |

START_TIME=60;
END_TIME=200;
LINES=50;  %Number of line sizes shown in the simulation
POSITIONS=21;
FOLDER='/home/sleigh/Dropbox/Research/Paper/data/Run May 27 2011, PIXELS=120, NEURONS_PER=20/RandD/';
SAMPLES=size(dir(FOLDER),1)-2; %Number of times the simulation was run

errors=cell(POSITIONS,LINES);

%mot_err=zeros(LINES,SAMPLES);
%line_size=zeros(LINES,1);

for i=0:SAMPLES-1,
    path=strcat(FOLDER,int2str(i),'.csv');
    %path=strcat('/home/sleigh/Dropbox/Research/Paper/data/Halligan/',int2str(i),'.csv');
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
    RC=.5;  %RC time constant
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
    legend('Line Position','Line Size','Prism Shift','Parietal Finger', ...
        'True Motor Error','True Perceptual Error','Leftward Error', ...
        'Rightward Error','Add');


    %Subsample the True Motor Error.  Only keep the sample at the end of a line
    %presentation.  Doing this will help remove transients.
    filt_mot_err=filter(alpha,[1 -(1-alpha)],X(:,6));
 
    for j=1:size(X,1),
        if X(j,1)>=START_TIME && X(j,1)<=END_TIME && (j==size(X,1) || X(j,3)~=X(j+1,3)),  %true when the line has just changed size
            errors{X(j,2)+11,X(j,3)}=[errors{X(j,2)+11,X(j,3)} , filt_mot_err(j)];
            %mot_err(X(j,3),i+1)=filt_mot_err(j);
            %line_size(X(j,3))=X(j,3).*2;
        end
    end
    i
end

mean_errors=zeros(POSITIONS,LINES);
std_errors=zeros(POSITIONS,LINES);
for i=1:size(errors,1),
    for j=1:size(errors,2),
        mean_errors(i,j)=mean(errors{i,j});
%         if isnan(mean_errors(i,j)),
%             mean_errors(i,j)=0;
%         end
        std_errors(i,j)=std(errors{i,j});
%         if isnan(std_errors(i,j)),
%             std_errors(i,j)=0;
%         end
    end
end

figure();
surf([2:2:100],[-10:10],mean_errors);
title('Mean Motor Error vs Line Size vs Line Position');
xlabel('Line Size [Pixels]');
ylabel('Line Position [Pixels]');
zlabel('Mean Motor Error [Pixles]');

figure();
surf([2:2:100],[-10:10],std_errors);
title('SD Motor Error vs Line Size vs Line Position');
xlabel('Line Size [Pixels]');
ylabel('Line Position [Pixels]');
zlabel('SD Motor Error [Pixles]');




% figure();
% plot(line_size,mot_err);
% title('Aggregate Motor Error vs Line Size');
% xlabel('Line Size [Pixels]');
% ylabel('Motor Error [Pixles]');
% 
% figure();
% errorbar(line_size,mean(mot_err'),std(mot_err'));
% title('Mean Motor Error vs Line Size (Error bars are STD)');
% xlabel('Line Size [Pixels]');
% ylabel('Motor Error [Pixles]');















%end