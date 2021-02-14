f = 1:10:100000;
w = 2*pi*f;

n = 1e-9;
u = 1e-6;
k = 1e3;

c1 = 10*n;
c2 = 470*n;
rf = 2.2*k;
ri = 2.2*k;
ro = 499;

% Z transform params
s = j.*w;
fs = 130*k*2; %2x converter switching frequency is the minimum for acceptable accuracy.
T = 1/fs;
ws = 2*pi*fs;
z1 = e.^(-s/fs);
sz = (2/T).*(1 - z1)./(1 + z1);


p0 = 1./(s.*ri*c1*ro);
p1 = (c1 + c2)./(rf*c1*c2);
z0 = 1/(rf*c2);
Hs = -(p0).*(s + z0)./(s + p1); %Without "fast lane"
Hfs = 1/ro - Hs;  %Add "fast lane" effect

%Direct representation of bilinear transform
pz0 = 1./(sz.*ri*c1*ro);
pz1 = (c1 + c2)./(rf*c1*c2);
zz0 = 1/(rf*c2);
Hz = -(pz0).*(sz + zz0)./(sz + pz1);
Hfz = 1/ro - Hz;

% Bilinear transform refactored for straightforward
% difference equation expression
% This can be implemented as 2 cascaded 1rst order IIR filters
zgain = (T/(2*ri*ro*c1)) * ((2*rf*c2)/(T - 2*rf*c2)) / ((T/2)*(c1 + c2)/(c1*c2*rf) - 1);
hz0 = (1 + z1)./(1 - z1);
hz1n = z1 + (2*rf*c2 + T)/(T - 2*rf*c2);
hz1d = z1 + (1 + (T/2)*(c1 + c2)/(c1*c2*rf)) / ((T/2)*(c1 + c2)/(c1*c2*rf) - 1);
hz1 = hz1n./hz1d;

hz = (1/ro) + zgain.*hz0.*hz1;  %Check against Hfz for algebra mistakes


subplot (2, 1, 1)
hold on
semilogx(f,20*log10(abs(Hfs)),"b")
semilogx(f,20*log10(abs(Hfz)),"r");
semilogx(f,20*log10(abs(hz)),"g");
subplot (2, 1, 2)
hold on
semilogx(f,angle(Hfs)*180/pi,"b")
semilogx(f,angle(Hfz)*180/pi,"r")
semilogx(f,angle(hz)*180/pi,"g")
