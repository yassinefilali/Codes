function [x,lmde,lmdi,mode]=sqp(simul,x,lmde,lmdi,maxit)
    n=size(x,1);
    eps=10^(-5);
    maxsim=maxit;
    [~,ce,ci,g,ae,ai,~]=feval(simul,4,x,lmde,lmdi);
    [~,~,~,~,~,~,M]=feval(simul,5,x,lmde,lmdi);
    
    k=1;
    mode=1;
        small = 10^(-5);
        big=10^(5);
        
        while (k<=maxit && (max(max(abs(g+ae'*lmde-ai'*lmdi)),max(abs(ce)))>eps || max(abs(min(lmdi,-ci))) > eps ))
            
            [L,d] = cholmod (M, small, big);
            M = L*diag(d)*L' ;
            %M = eye(n);
            [d,~,~,~,LAMBDA]=quadprog(M,g,ai,-ci,ae,-ce);
            x=x+d
            lmde = LAMBDA.eqlin;
            lmdi = LAMBDA.ineqlin;
            [~,ce,ci,g,ae,ai,~]=feval(simul,4,x,lmde,lmdi);
            [~,~,~,~,~,~,M]=feval(simul,5,x,lmde,lmdi);
            k= k +1;
            
   
         if (max(max(abs(g+ae'*lmde+ai'*lmdi)),max(abs(ce)))<eps && max(abs(min(lmdi,-ci))) < eps )
             mode = 0;
                return
         elseif k>maxit
             mode = 2;
        return
         end
         end
end
