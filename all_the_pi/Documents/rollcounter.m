%% Roll Counter
%
% I don't entirely remember what this does
clear,clc,close all
format compact

%% 
rotations = 100;	% 1 rotation = 2*pi() radians
ft_to_mm = 304.8;	% 1ft = 304.8mm
paper_per_roll = 150 * ft_to_mm;	% mm
pi2 = 2*pi();	% 2*pi, dimensionless
t = 0.1;	% paper thickness, mm
r_co = 15/2;	% core radius outer, mm
rolls_used = 0;	% number of full rolls depleted
total_rolls = 11;	% from piday.m need 11 rolls of paper
					% Assume 0mm splice length on each end 
					% of the roll of paper. 

% Preallocation
r = zeros([rotations, 1]);
s = zeros([rotations, 1]);
r_paper = zeros([rotations, 1]);
theta = zeros([1, rotations]);	% row vector!!

% Initial conditions
r(1, 1) = r_co;	% radius to outer paper layer, mm
r_paper(1, 1) = r(1, 1) - r_co;	% thickness of just the layers of paper, mm
s(1, 1) = 0;	% length of paper, mm
theta(1) = 0;

i = 2;

while rolls_used <= 11
	theta(i) = round(theta(i-1) + pi2, 4);	% radians
	dtheta = round(theta(i) - theta(i-1), 4);	% change in theta, should be 2*pi()
	r(i, 1) = radius(r(i-1, 1), dtheta, t);	% radius to outermost layer of paper, mm
	s(i, 1) = s(i-1, 1) + linear_paper_length(r(i, 1), dtheta);	% linear length of paper, mm
	r_paper(i, 1) = r(i, 1) - r_co;	% thickness of the layers of paper, mm
	
	
	i = i + 1;
	rotations = i;
end


%% Functions

function [all_rolls, roll_remaining, incr] = check_roll(rolls_used, s, s_per_roll)
	%[roll_remaining, incr] = check_roll(rolls_used, s, s_per_roll)
	%
	% Inputs:
	% rolls_used = the number of rolls currently used
	% s = [s_previous, s_current] = a 1x2 row vector containing the sum of all
	% previous s values in element 1 and the current s value in element 2. Units
	% are mm.
	% s_per_roll = the linear length of paper per roll. Default is 45,720mm.
	%
	% Outputs:
	% all_rolls = a struct containing information on the rolls
	% roll_remaining = the linear length of paper remaining on the roll, mm.
	% incr = a boolean indicating whether or not the calling program should
	% incrememnt the number of rolls used. 
	if numel(s) < 2
		error('s must be a 1x2 row vector');
	end
	if nargin < 1 || isempty(rolls_used)
		rolls_used = 0;
	end
	if nargin < 2 || isempty(s)
		error('s is a required input');
	end
	if nargin < 3 || isempty(s_per_roll)
		s_per_roll = 150*304.8;	% 150ft * 304.8mm/ft
	end
	s_previous = s(1);	% sum of all previous paper lengths, mm
	s_current = s(2);	% most recent paper length, mm
	
	kk = rolls_used + 1;	% index variable for the current roll
	all_rolls(kk).paper_len = s_per_roll;
	all_rolls(kk).paper_remaining = all_rolls(kk).paper_len - s_previous;
	
	new_paper_remaining = all_rolls(kk).paper_remaining - s_current;
	if new_paper_remaining <= 0
		incr = true;
		
	end
	
	
end


function rr = radius(r0, thetai, t)
	%rr = radius(r0, theta, t)
	%
	% Inputs:
	% r0 = initial radius, mm
	% thetai = angle of rotation, radians. Must be even intervals of 2*pi().
	% t = thickness of paper, mm
	two_pi = round(2*pi(), 4);	
	if round(mod(thetai, two_pi), 0) ~= 0
		disp(thetai)
		disp(mod(thetai, 2*pi()))
		error('theta must be an integer multiple of 2*pi');
	end
	rr = r0 + floor(thetai/two_pi)*t;
	clearvars thetai r0
end
function s = linear_paper_length(ri, thetai)
	%s = linear_paper_length(r, theta)
	%
	% Inputs:
	% ri = current radius, mm
	% thetai = angle of rotation, radians. Must be an integer multiple of 2*pi().
	two_pi = round(2*pi(), 4);
	if round(mod(thetai, two_pi),0) ~= 0
		error('theta must be an integer multiple of 2*pi');
	end
	s = ri*thetai;	% mm
	clearvars thetai ri
end

