%%
clear,clc,close all
format compact

%%
M012 = [0 0 0; 1 0 0; 0 1 0; 1 1 0; 0 0 1; 1 0 1; 0 1 1; 1 1 1];

%{
% % Full step
% Step.full.m0 = M012(1,1);
% Step.full.m1 = M012(1,2);
% Step.full.m2 = M012(1,3);
% 
% % Half step
% Step.half.m0 = M012(2,1);
% Step.half.m1 = M012(2,2);
% Step.half.m2 = M012(2,3);
% 
% % 1/4 step
% Step.quarter.m0 = M012(3,1);
% Step.quarter.m1 = M012(3,2);
% Step.quarter.m2 = M012(3,3);
% 
% % 1/8 step
% Step.eigth.m0 = M012(4,1);
% Step.eigth.m1 = M012(4,2);
% Step.eigth.m2 = M012(4,3);
% 
% % 1/16 step
% Step.sixteenth.m0 = M012(5,1);
% Step.sixteenth.m1 = M012(5,2);
% Step.sixteenth.m2 = M012(5,3);
% 
% % 1/32 step
% Step.thirtysecond.m0 = M012(6,1);
% Step.thirtysecond.m1 = M012(6,2);
% Step.thirtysecond.m2 = M012(6,3);
%}

%% Full Step
% Full step can be bypassed for hardware by not activating any of the pins
% since this is already the default from the DRV 8825 board. 
Resolution.full = M012(1,:);

%% Half step, Eigth step
% half step shares a common M0 with 1/8th step
% Half step = [HIGH LOW LOW]
% Eigth step = [HIGH HIGH LOW]
% 
% Try to find a way to combine these via variable current throughput 
%	from the GPIO pin
% 
% For half and eigth step only pins M0 and M1 need be connected
Resolution.half = M012(2,:);
Resolution.eigth = M012(4,:);


Resolution.quarter = M012(3,:);
Resolution.sixteenth = M012(5,:);
Resolution.thirtysecond = M012(6,:);


