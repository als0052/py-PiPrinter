%% Find the size of the giant paper spool
%{
% Assuming every 11th line is a blank (whitespace) line, 
% there will be 91,668 lines @ 5mm center-center line spacing
% thus 458,340mm of paper will be needed
%
% NOTE: With the thermal printer a new line spacing might be required for these 
%		calculations. 
%
% Assume:
% 1 roll of paper = 150 ft
% roll splices use 5mm of each end (10mm total per roll) (not factored into calculations).
% 
%}
clear,clc,close all
format compact

%% Fill the spool with 458.34 meters of paper
% Constants
rotations = 100;	% 1 rotation = 2*pi() radians
ft_to_mm = 304.8;	% 1ft = 304.8mm
paper_per_roll = 150 * ft_to_mm;	% mm
pi2 = 2*pi();	% 2*pi, dimensionless
t = 0.1;	% paper thickness, mm
r_co = 15/2;	% core radius outer, mm

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

% Solve
i = 2;
while s <= paper_per_roll*11 %s <= 458340	% 458,340 mm
	theta(i) = round(theta(i-1) + pi2, 4);	% radians
	dtheta = round(theta(i) - theta(i-1), 4);	% change in theta, should be 2*pi()
	r(i, 1) = radius(r(i-1, 1), dtheta, t);	% radius to outermost layer of paper, mm
	s(i, 1) = s(i-1, 1) + linear_paper_length(r(i, 1), dtheta);	% linear length of paper, mm
	r_paper(i, 1) = r(i, 1) - r_co;	% thickness of the layers of paper, mm
	i = i + 1;
	rotations = i;
end

if mod(round(s(end) / paper_per_roll, 2), 1) ~= 0
	% number of whole rolls needed
	% fractional roll case
	no_rolls = ceil(s(end) / paper_per_roll);
else
	% number of whole rolls needed
	% integer roll case
	no_rolls = s(end) / paper_per_roll;
end

% Output
fprintf("Rotations:\t%d\n", rotations);
fprintf("Radius of spool from geometric center:\t%.2f mm\n", r(end));
fprintf("Radius of spool core:\t%.2f mm\n", r_co);
fprintf("Thickness of layers of paper:\t%.2f mm\n", r_paper(end));
fprintf("Linear paper length:\t%.2f m\n", s(end)/1000);
fprintf("Number of rolls of paper:\t%.0f rolls\n", no_rolls);
clearvars i pi2 dtheta r_co theta

%% Functions
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
