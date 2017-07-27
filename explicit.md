# finite-difference-method-for-Eu-Am-option-pricing
implicit, explicit and Crank-Nicolson method to price option.
% this is explicit method for EU  put option

clear
clc
%S,E,sig,r,T,
 M=1600; % Number of time points
 N=160; % Number of share price points
 E=10;
 S=12;
 %Smin=0;
 Smax=15;
 ds=Smax/N;
 T=1;
 sd=0.2;
 r=0.05;
 dt=T/M; % Time step

 V=zeros(M+1,N+1);
for i=1:N+1
    V(M+1,i)=max(E-(i-1)*ds,0);    %T
end

for j = 1:M+1               
  V(j,N+1)=0;               %V(Smax,t)
end

 for j=1:M+1
    %  V(j,1)=E*exp(-r*(T-dt*(j-1)));   %S=0
    V(j,1)=E;
 end

 a=zeros(N);
 b=zeros(N);
 c=zeros(N);
 for i=1:N
     a(i)=0.5*dt*((sd^2)*(i^2)-r*i);
     b(i)=1-dt*((sd^2)*(i^2)+r);
     c(i)=0.5*dt*((sd^2)*(i^2)+r*i);
%        a(i)=(1 + r*dt)^-1 * (-1/2*r*i*dt + 1/2*sd^2*i^2*dt);
%        b(i)=(1 + r*dt)^-1 * (1 - sd^2*i^2*dt);                   %i 代表钱 i is money
%        c(i)=(1 + r*dt)^-1 * (1/2*r*i*dt + 1/2*sd^2*i^2*dt);
 end

 for j=M:-1:1
     for i=2:N
%          a=(1 + r*dt)^-1 * (-1/2*r*i*dt + 1/2*sd^2*i^2*dt);
%          b=(1 + r*dt)^-1 * (1 - sd^2*i^2*dt);                   %i 代表钱 means money
%          c=(1 + r*dt)^-1 * (1/2*r*i*dt + 1/2*sd^2*i^2*dt);
         V(j,i)=a(i)*V(j+1,i-1)+b(i)*V(j+1,i)+c(i)*V(j+1,i+1);
     end
 end
 value=[];
 Put=zeros(0,N);
 Call=zeros(0,N);
 Price=(0:ds:15);
 for a=1:1:160
 d1=(log((ds*a)/E)+(r+0.5*sd^2)*(1))/(sd*sqrt(1));
 d2=d1-sd*sqrt(1);
 
 valueofn_minus_d1=normpdf(-d1,0,1);
 valueofn_minus_d2=normpdf(-d2,0,1);
 
 value(a+1)=E*exp(-r*(1))*valueofn_minus_d2-ds*a*valueofn_minus_d1;
 
 
[Call(a+1),  Put(a+1)]=blsprice(Price(a+1),10,0.05,1,0.2);
 end
 Put(1)=E*exp(-r*1);
 V(1,1)=E*exp(-r*1);
 plot (ds*(0:N),V(1,:));
  hold on
  %plot([0,E],[E,0]);
 plot(ds*(0:N),Put);
