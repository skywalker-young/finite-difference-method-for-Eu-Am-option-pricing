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
 
     a=(1/2)*dt*((r-D)*j-sd^2*j.^2);
b=1+(sd^2*j.^2+(r-D))*dt;
c=(-1/2)*dt*((r-D)*j+sd^2*j.^2);
 
%     for i=1:N 
%      a(i)=0.5*sd^2*i^2*dt-(r-D)*dt*i;
%      b(i)=1-sd^2*i^2*dt-r*dt;
%      c(i)= (r-D)*dt*i+0.5*sd^2*i^2*dt;
%  end
 


L=diag(a(3:N),-1)+diag(b(2:N))+diag(c(2:N-1),1);
[low,up]=lu(L);
C=zeros(size(L,2),1);
% for i=M:-1:1  %%%时间
%     
%     temp=zeros(N,1); %跟钱有关
% 
%     temp(1)=a(2)*V(i+1,1);
%     temp(end)=c(N)*V(i+1,N+1);
%     
%     V(2:N,i)=up\(low\(V(2:N,i+1)-temp))
% end.

 
%  utemp=n*max(Z,linspace(0,Smax,N+1));
%  utemp=utemp(2:N)';
for i=M:-1:1
    
    C(1)=a(2)*V(i,1);
    C(end)=c(end)*V(i,end);
    
   V(i,2:N)=up\(low\(V(i+1,2:N)'-C));
   V(i,2:N)=max(V(i,2:N),n*ds*(2:N));
%     qtemp=up\(low\(V(i+1,2:N)'-C));
%     index=find(qtemp<utemp );
%     qtemp(index)=utemp(index);
%    V(i,2:N)=qtemp;
end
 
 
% utemp=max(Z,linspace(0,Smax,N+1));
% utemp=utemp(2:N)';
% for loop=M:-1:1         %时间
%     temp=zeros(N-1,1);   %钱
%     temp(1)=a(2)*V(loop+1,1) ;  %Matrix(1,loop+1);
%     temp(N-1)=c(N)*V(loop+1,N+1);  %   Matrix(N+1,loop+1);
%    % qtemp=L\((V(loop+1,2:N))'-temp);     
%    qtemp=up\(low\(V(loop+1,2:N)'-temp));
%     indx=find(qtemp<utemp);
%     qtemp(indx)=utemp(indx);
%    V(loop,2:N)=qtemp;
% end
  plot (ds*(0:N),V(1200,:));
  hold on;
 % plot (ds*(0:N),V(1000,:));
 plot (ds*(0:N),V(1,:));
 plot([0,Smax],[0*n,Smax*n]);
