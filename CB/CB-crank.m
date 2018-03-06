clear;
clc;

Z=100; % 债券的回报
r=0.07; %固定利率
sd=0.2;
D=0.01;
T=1;  % time to maturity
S=50;
Smax=160;
N=160;
M=1600;
ds=Smax/N;   %钱
dt=T/M;   %时间
n=1.5;  %1份债券换1.5份股票
V=zeros(M+1,N+1);

%边界条件
% Smax 时候，选择债转股
 for i=1:1:M+1
     V(i,N+1)=n*Smax;
     
 end
 

for i=1:1:N+1
    V(M+1,i)= max(Z,n*ds*i);
end

for i=1:1:M+1
    V(i,1)=Z*exp(-r*(T-dt*(i-1)));
end

%   j=0:N;
%      a =0.5*(r-D)*j*dt-0.5*sd^2*j.^2*dt;
%      b =1+r*dt+sd^2*j.^2*dt;
%      c= -0.5*(r-D)*dt*j-0.5*sd^2*j.^2*dt;
  j=0:N;
 
      
a=(dt/4)*(sd^2*(j.^2) - (r-D)*j);
b = -(dt/2)*(sd^2*(j.^2) + (r-D));
c = (dt/4)*(sd^2*(j.^2) + (r-D)*j);
 

C = -diag(a(3:N),-1) + diag(1-b(2:N)) - diag(c(2:N-1),1);
[L,U] = lu(C);
DD = diag(a(3:N),-1) + diag(1+b(2:N)) + diag(c(2:N-1),1);

 for i=0:1:160
 temp(1,i+1)=max( i*ds-Z,0);
 end
 temp=temp(2:N)' ;
% Solve at each node
 offset = zeros(size(DD,2),1);
for i=M:-1:1
    offset(1) = a(2)*(V(i,1)+V(i+1,1));
       offset(end) = c(end)*(V(i,end)+V(i+1,end));
   V(i,2:N)= U\(L\(DD*V(i+1,2:N)' + offset));
     
   V(i,2:N)=max(V(i,2:N),n*ds*(2:N));
%     qtemp=up\(low\(V(i+1,2:N)'-C));
%     index=find(qtemp<utemp );
%     qtemp(index)=utemp(index);
%    V(i,2:N)=qtemp;
end
  plot (ds*(0:N),V(1200,:));
  hold on;
 % plot (ds*(0:N),V(1000,:));
 plot (ds*(0:N),V(1,:));
 plot([0,Smax],[0*n,Smax*n]);
