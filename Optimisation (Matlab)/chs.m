function [e,ce,ci,g,ae,ai,hl,indic] = chs(indic,xy,lmde,lmdi)
    global LB A B R S ;
    n=size(xy,1);
    nn=n/2;
    [e,ce,ci,g,ae,ai,hl]=deal(0);
    switch indic
        case 1
            X=[0;xy(1:nn);A];
            Y=[0;xy(nn+1:n);B];
            plot(X,Y,'-ob');
            hold on;
            if(size(R)~=0)
            xlin=linspace(1.1*min(X),1.1*max(X));
            pl=plot(xlin,max(R*ones(1,size(xlin,2))+S*xlin,[],1),'r');
            set(pl,'LineWidth',2.5)
            plancher;
            end
            indic = 0;
            

        case 2
	    p = size(s,1);
            e=(LB'*([0;xy(nn+1:n)]+[xy(nn+1:n);b]))/2;
            ce= sparse([([xy(nn+1:n);b]-[0;xy(nn+1:n)]).^2+([xy(1:nn);a]-[0;xy(1:nn)]).^2 - LB.^2]);
            ci = zeros(nn*p,1);
            for j=1:p
                for i=1:nn
                    ci(i+(j-1)*nn)=r(j)+xy(i)*s(j)-xy(nn+i);
                end
            end
               
            indic = 0;
        case 4
           
            e=(LB'*([0;xy(nn+1:n)]+[xy(nn+1:n);B]))/2;
            ce= sparse([([xy(nn+1:n);B]-[0;xy(nn+1:n)]).^2+([xy(1:nn);A]-[0;xy(1:nn)]).^2 - LB.^2]);
            if size(S)~=0
            p = size(S,1);
            ci = zeros(nn*p,1);
            for j=1:p
                for i=1:nn
                    ci(i+(j-1)*nn)=R(j)+xy(i)*S(j)-xy(nn+i);
                end
            end
            else
                ci=zeros(nn,1);
            end
            g=sparse([ zeros(nn,1);(LB(1:nn)+LB(2:nn+1))/2]);
            
            ae=sparse(2*[[(diag(xy(1:nn))-diag([0;xy(1:nn-1)]));zeros(1,nn)]-[zeros(1,nn);(diag([xy(2:nn);A])-diag(xy(1:nn)))],[[(diag(xy(nn+1:n))-diag([0;xy(nn+1:n-1)]));zeros(1,nn)]-[zeros(1,nn);(diag([xy(nn+2:n);B])-diag(xy(nn+1:n)))]]]);
            
	   if size(S)~=0
            ai=[S(1)*eye(nn),-1*eye(nn)];
                for i=2:p
                ai=[ai;S(i)*eye(nn),-1*eye(nn)];
                end
       else
            ai=zeros(nn,n);

            indic = 0;
       end
        case 5
            if (size(lmde,1)==nn+1)
                hx = zeros(nn,nn);
                for k=1:nn+1
                    if (k<=nn) hx(k,k)=hx(k,k)+2*lmde(k); end
                    if (k>=2) hx(k-1,k-1)=hx(k-1,k-1)+2*lmde(k); end
                    if (k<=nn && k>=2)
                        hx(k,k-1)=hx(k,k-1)-2*lmde(k);
                        hx(k-1,k)=hx(k-1,k)-2*lmde(k);
                    end
                end
                hl = sparse([[hx,zeros(nn,nn)];[zeros(nn,nn),hx]]);
                indic = 0;
            else
                indic = 1;
            end
        otherwise
            indic = 1; 
    end
end
