clear;
clc;

Z=100; % 债券的回报
r=0.05; %固定利率
sd=0.2;
D=0.01;
T=1;  % time to maturity
S=15;
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

a=zeros(N);
 b=zeros(N);
 c=zeros(N);
 
 for i=1:N 
     a(i)=0.5*sd^2*i^2*dt-(r-D)*dt*i;
     b(i)=1-sd^2*i^2*dt-r*dt;
     c(i)= (r-D)*dt*i+0.5*sd^2*i^2*dt;
 end
 
 %这段话可以在循环里一句解决
%    for i=0:1:160
%  temp(1,i+1)=max( i*ds-Z,0);
%    end
%  temp=temp(2:N);
%  
 for j=M:-1:1
     for i=2:N
%          a=(1 + r*dt)^-1 * (-1/2*r*i*dt + 1/2*sd^2*i^2*dt);
%          b=(1 + r*dt)^-1 * (1 - sd^2*i^2*dt);                   %i 代表钱
%          c=(1 + r*dt)^-1 * (1/2*r*i*dt + 1/2*sd^2*i^2*dt);
         V(j,i)=a(i)*V(j+1,i-1)+b(i)*V(j+1,i)+c(i)*V(j+1,i+1);
          V(j,i)=max(V(j,i),n*ds*i);
          %V(j,i)=max(V(j,i),temp(i-1));
     end
 end
 plot (ds*(0:N),V(1,:));
 hold on;
  plot (ds*(0:N),V(1200,:));

 plot([0,Smax],[0*n,Smax*n]);
