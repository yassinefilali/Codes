function [ x,lme,lmi,info ] = sqp( simul,x,lme,lmi,options )


k=1;


%Grandeurs de cholmod
small=10^-5;
big=10^5;

% initialisation des variables de sortie
  info       = [];
  info.iter  = 0;
  info.simul = 0;

  %taille du probleme 
n=size(x,1);
me=size(lme,1);
mi=size(lmi,1);

lm0=[zeros(n,1);lme;lmi];
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %lm0 is an n+mi+me vector, giving an initial guess of the dual solution
    %or Lagrange multiplier associated with the bound constraints
    %(components 1:n), the linear inequality contraints (components n+1:n+mi) 
    %and the equality contraints (components n+mi+1:n+mi+me);
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
 x0=zeros(n,1);
% Les parametres de la fonction qplam 
     %appel au simulateur 
    [~,ce,ci,g,ae,ai,~,indic]=feval(simul,4,x,lme,lmi);
    if indic~=0
        fprint(fout, 'erreur dans le simulateur');
    end
    [~,~,~,~,~,~,M,indic]=feval(simul,5,x,lme,lmi); %recuperation de la hessien du lagrangien 
    if indic~=0
     fprint(fout, 'erreur dans le simulateur');
    end
    %les limites sur x 
    lbx=(-inf)*ones(n,1);
    ubx=(+inf)*ones(n,1);
    %les limites sur les contraintes inégaliés 
    lbi=(-inf)*ones(mi,1);
if indic==1 
    info.status=1;
end
       while (k<options.iter && k<options.simul)
           %(k<=maxit && (max(max(abs(g+ae'*lme-ai'*lmi)),max(abs(ce)))>eps || max(abs(min(lmdi,-ci))) > eps ))
            gradLagrangien=g'+lme'*ae+lmi'*ai;
        if (max(max(abs(gradLagrangien)),max(max(abs(ce)),max(abs(min(lmi,-ci))))) < options.tol(1))
             info.status=0; %terminaison normale
             return
        end
            [L,d] = cholmod (M, small, big);
            M = L*diag(d)*L' ;
            %M = eye(n);
            [d,lm,info]=qpalm(g,M,lbx,ubx,ai,lbi,-ci,ae,-ce,x0,lm0);
            x=x+d;
            lmi=lm(n+1:n+mi);
            lme=lm(n+mi+1:n+me+mi);
            [~,ce,ci,g,ae,ai,~]=feval(simul,4,x,lme,lmi);
            [~,~,~,~,~,~,M]=feval(simul,5,x,lme,lmi);
            k= k +1;
            feval(simul,1,x,lme,lmi);
        end
   
    if (max(max(abs(g+ae'*lme+ai'*lmi)),max(abs(ce)))<eps && max(abs(min(lmi,-ci))) < eps )
        mode = 0;
    elseif k>maxit
        mode=2;
    end

