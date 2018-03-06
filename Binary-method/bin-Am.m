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

V=zeros(N+1);
V(:,end)=max(S(:,end)-K,0);
for j=N:-1:1
    for i=1:j
        V(i,j)=sum(V(i:i+1,j+1))*p/exp(r);
    end
    temp=max(S(:,j)-K,0);
    ind=find(V(:,j)<temp);
    V(ind,j)=temp(ind);
end

V(1,1)
