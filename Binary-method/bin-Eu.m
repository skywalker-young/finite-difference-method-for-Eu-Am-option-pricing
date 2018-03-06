clear
S=50;sigma=0.1;r=0.05;T=1;N=4;dt=T/N;K=50;
d=2*exp(r*dt)/(1+exp(2*sigma*sqrt(dt)));
u=2*exp(-r*dt)*exp(2*sigma*sqrt(dt))/(1+exp(2*sigma*sqrt(dt)));
p=0.5;
S(1,1)=S;
for j=2:N+1
    for i=1:j
        S(i,j)=S(1,1)*u^(j-i)*d^(i-1);
    end
end

Q=zeros(N+1);
Q(1,1)=1;
for j=2:N+1
    for i=1:j
        if i==1
            Q(i,j)=Q(i,j-1)*p/exp(r);
        elseif i==j
            Q(i,j)=Q(i-1,j-1)*p/exp(r);
        else
            Q(i,j)=(Q(i-1,j-1)+Q(i,j-1))*p/exp(r);
        end
    end
end
% V=sum(max(K-S(:,end),0).*Q(:,end)) %¿´µøÆÚÈ¨ÓÃÕâÌõ
V=sum(max(S(:,end)-K,0).*Q(:,end))% ¿´ÕÇÆÚÈ¨ÓÃÕâÌõ
