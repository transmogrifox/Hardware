u=1e-6;
n=1e-9;
p=1e-12;
k=1e3;

e = exp(1);

fsw=125*k %Switching frequency
Tsw = 1/fsw
wm=2*pi*fsw;
w=0;
nfs=1.0;
w=(2*pi*10:1:nfs*wm);
fr = w/(2*pi);
s=j*w;
z=e.^(-s*Tsw);

%% Flyback converter open loop gain
Nps = 54/8; %Transformer Primary-Secondary turns ratio
L=580*u; %Primary inductance
vin = 375; %Input voltage
vin_min = 85; %Minimum input voltage
vout = 13.25; %Output voltage
iout = 3; %Output current

%% Current sensing node
Rcs = 0.33; %Current sense resistor
R2 = 475;
R3 = 4.02*k;
R8 = 237*k*2;
R4 = 10*k;
R5 = 475;
R6 = 499*k;
C15 = 1*p;
Rg = 1/(1/R2 + 1/R3 + 1/R8);
Rf = R5;
Ry = Rg+Rf;
Rx = R6;
Cx = C15;
Rpll = Ry*R4/(Ry+R4)
Rpcs = 1/(1/(R5+R6*R4/(R6+R4)) + 1/R3 + 1/R8)
gipk = (1/Rcs)*(Rpcs+R2)/Rpcs


%% Power stage loading (output impedance)
ncout = 3;
cout = ncout*470*u; 
cload = 470*u;
lf = 0.5*u; %Filter inductor 
cesr = 0.012; %capacitor ESR
lesr = 0.01; %Filter inductor ESR

%% Error amplifier and compensation components
cp = 100*p; %HF roll-off parallel to r-c P-Z pair
cf = 22*n; %Low frequency pole
rf = 121*k; %Forms Zero with cs
ri = 33*k; %Input feed resistor 
ro = 1.1*k;  %Resistor in series with optocoupler LED
ctr = 0.75;  %Optocoupler CTR
fc_opto = 80*k; %Optocoupler cut-of frequency (pole frequency)

%% Error amplifier transfer function 
p0 = 1./(s.*ri*cp*ro);
p1 = (cp + cf)./(rf*cp*cf);
z0 = 1/(rf*cf);
p_opt = 1/(2*pi*fc_opto);
H_EA = -(p0).*(s + z0)./(s + p1); %Without "fast lane"
H_LED = 1/ro - H_EA;  %Add "fast lane" effect
H_comp = gipk*H_LED*ctr./(s*p_opt+1);

%Then the stupidity pole
g_stupid = Rg/(Rg+Rf)
H_stupid = g_stupid*Rpll*(s.*Rx*Cx + 1)./(s.*(Rpll+Rx)*Cx + 1);

%% Slope compensation required for <6dB valley current peaking 
mcmp=(3*vout*Nps-vin_min)/(4*L)

%% Computed system parameters
idg = iout/Nps;
vdg=vout*Nps;
vcg=vin-2;
D=vdg/(vcg+vdg)
Dp = 1-D;
mc=vcg/L;
md=vdg/L;

%% Control-to-valley small signal gain
alpha = (mc+md) / (mc + mcmp);
hz = alpha./(1- (1-alpha)*z);  %%Transfer function, iv/ic 

%% Valley-to-average small signal gain
Iv = idg*(vcg+vdg)/vcg - (Tsw/(2*L))*vcg*vdg/(vcg+vdg) %%Steady state valley current
hdg = Nps*(Iv/(mc+md)).*(mc/Iv-s); %% Small-signal valley-to-average current <-Turns ratio applied here

%% Output pulse shape (influences group delay)
gDG = 2/(Dp^2*Tsw^2*md + 2*Dp*Tsw*Iv);
HDG = gDG*(Iv+md*Dp*Tsw).*((1 - e.^(-s*Dp*Tsw))./s).*e.^(-s*D*Tsw) - gDG*md*((1 - (1+s*Dp*Tsw).*e.^(-s*Dp*Tsw))./(s.^2)).*e.^(-s*D*Tsw);

%% Output impedance network
rout = vout/idg
zlf = s*lf + lesr;
zcl = 1./(s*cload) + cesr;
zcout = 1./(s*cout) + cesr/ncout;
zl = zlf+zcl*rout./(rout+zcl);
zout = zl.*zcout./(zcout+zl);

%% Original design had feedback tapped from output filter
zload = zcl*rout./(rout+zcl);
H_out = zload./(zlf + zload);  % Left out of transfer function for improved design

%%
%% Plot final system 
%%
%% VOUT->[Error Amp]->[Stupid Comp]->[Valley Current]->[Average Current]->[Group Delay]->[Zout]
%%

subplot(2,1,1)
semilogx(fr,20*log10(abs(H_comp.*H_stupid.*hz.*hdg.*HDG.*zout)), 'r', 'linewidth', 1.5)
%semilogx(fr,20*log10(abs(H_out)), 'r', 'linewidth', 1.5)
%semilogx(fr,20*log10(abs(H_stupid)),"r", "linewidth", 1.5)
%semilogx(fr,20*log10(abs(H_comp)))
%semilogx(fr,20*log10(abs(hdg)))
%semilogx(fr,20*log10(abs(HDG)))
%semilogx(fr,20*log10(abs(zout)))
subplot(2,1,2)
phase = unwrap(angle(-H_stupid.*H_comp.*HDG.*hdg.*hz.*zout));
semilogx(fr,180*phase/pi, 'b', 'linewidth', 1.5)
%semilogx(w,180*(unwrap(angle(HDG)))/pi)
%subplot(3,1,3)

%phase = unwrap(angle(HDG));
lp=length(phase);
lp1 = lp-1;
p1 = phase(1:lp1);
p0 = phase(2:lp);
dp = p1 - p0;
wp = w(1:lp1);
%semilogx(wp/(2*pi),dp, 'g', 'linewidth', 1.5)

gd = 1e6*dp(392698)
fx = 1e6/gd
