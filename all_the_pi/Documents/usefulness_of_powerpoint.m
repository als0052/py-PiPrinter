%%
clear,clc,close all
format compact

%%

t = linspace(0, 30, 250);
usefulness = t.^2;

f = figure();
p = plot(t, usefulness);
xlabel('Days');
ylabel({'Usefulness', '(inch/inch)'});
title({'Usefulness of', 'PowerPoint'});
grid on
