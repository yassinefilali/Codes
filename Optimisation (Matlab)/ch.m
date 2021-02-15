
clear all;
addpath qpalm;
global LB A B R S; % varibales globals du probleme 

maxit=1000;
maxsim=1000;
simul='chs';		% nom du simulateur
%%%%les options de simulations %%%%%%%
    %Les tolerances 
  options.tol(1) = 1.e-9;    % sur le gradient du lagrangien
  options.tol(2) = 1.e-9;    % sur les contraintes d'egalite
  options.tol(3) = 1.e-9;    % sur les contraintes d'inegalite
  options.tol(4) = 1.e-9;    %sur la positivite de multiplicateurs et la complementarite

  options.iter  = maxit;      % max iterations
  options.simul = maxsim;     % max simulations
  
  options.dxmin = 1.e-20;
  options.verb  = 1;
%les parametres du probleme 
%cas test 4-a
% LB=[.7 .5 .3 .2 .5];
% A=1; B=-1; % coordonnées du dernier point de la chaine 
% xy= [ .2 .4 .6 .8 1 1.5 1.5 1.3]';
% R ; S;
% %cas test 4-b
 LB=[.2 .2 .2 .3 .3 .5 .2 .2 .3 .1]';%longuers des barres de la chaine 
 A=1;B=0;
 R=[-0.25;-0.5];S=[-0.5;0];
 xy=[.1 .2 .3 .4 .5 .6 .7 .8 .9 -0.5 -0.9 -1.2 -1.4 -1.5 -1.4 -1.2 -0.9 -0.5]';

nn=size(xy,1)/2;%le nombre total des noeuds
nb=nn+1; %nombre de barre
p=size(R,1);
lme=ones(nn+1,1); %mutilplicateur des contraintes d'égalité 
if p~=0
    lmi=ones(p*nn,1);%mutilplicateur des contraintes d'inégalité 
else 
    lmi=zeros(nn,1);
end
%%%% La phase de simulation %%%%
[e,ce,ci,g,ae,ai,~,indic]=chs(4,xy,lme,lmi);
[~,~,~,~,~,~,hl,indic]=chs(5,xy,lme,lmi);
[x, lme, lmi, info]= sqp (simul, xy, lme, lmi, maxit);
[~,~,~,~,~,~,~,indic]=chs(1,x,lme,lmi);


