%% Type II compensator with optocoupler fast-lane
%
%   [Vfb]--*-----------------*
%          |                 |
%          |                 \
%          \                 /
%          / Ri              \ Ro
%          \                 /
%          /                 |
%          |                 __
%          |            LED _\/_ ~^~>[CTR]-->[Iemitter]
%          |      Cp         |
%          *------||---------*
%          |                 |
%          |   Cf     Rf     |
%          *---||---/\/\/----*
%          |                 |
%          |                 |
%          |               \____
%          |                 /\ \
%          *----------------/  \
%          |               ------
%          |                  |
%          /                  |
%          \  Rdc_bias        |
%          /                  |
%          \                  |
%          |                  |
%          *------------------*
%                             |
%                           -----
%                            ---
%                             -
%          Iemitter(s)
% Hc(s) = -------------
%            Vfb(s)
%

%%
%% Engineering notation shorthand
%%
p = 1e-12;
n = 1e-9;
u = 1e-6;
k = 1e3;

%%
%% Plotting ranges
%%

%Converter switching frequency only interesting 
%for setting plot limits
fsw = 125*k;
%Multiples of fsw to plot
nfs = 2;
f = 1:10:(fsw*nfs);
w = 2*pi*f;
s = j*w;

%%
%% Compensator component values
%%
Cp = 47*p;
Cf = 4.7*n;
Rf = 150*k;
Ri = 33.2*k;
Ro = 1*k;
fc_opto = 80*k;
CTR = 0.75;

%%
%% System transfer functions
%% 
p0 = 1./(s.*Ri*Cp);
p1 = (Cf + Cp)./(Rf*Cf*Cp);
z0 = 1/(Rf*Cf);
wopt = 2*pi*fc_opto;
popt = CTR*wopt./(s + wopt);
Hs = -(1/Ro)*p0.*(s + z0)./(s + p1); %Without "fast lane"
Hfs = (1/Ro - Hs).*popt;  %Add "fast lane" effect

%%
%% Plot transfer function
%%
subplot (2, 1, 1)
hold on
semilogx(f,20*log10(abs(Hfs)),"r","linewidth",1.5)
#set(gca, "linewidth", 4, "fontsize", 12)
subplot (2, 1, 2)
hold on
semilogx(f,angle(Hfs)*180/pi,"b","linewidth",1.5)
#set(gca, "linewidth", 4, "fontsize", 12)
