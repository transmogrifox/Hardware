u=1e-6;
n=1e-9;
p=1e-12;
k=1e3;

%% Flyback converter open loop gain
fsw=125*k %Switching frequency
Tsw = 1/fsw
Nps = 54/8; %Transformer Primary-Secondary turns ratio
L=580*u; %Primary inductance
vin = 88; %Input voltage
vin_min = 75; %Minimum input voltage
vout = 12; %Output voltage
iout = 3; %Output current
Rcs = 0.4; %Current sense resistor
gipk = 1.4/Rcs;
Rfeed = 475; %convert opto current to voltage at current sense node

%% Power stage loading (output impedance)
ncout = 3;
cout = ncout*470*u; 
cload = 470*u;
lf = 1*u; %Filter inductor 
cesr = 0.02; %capacitor ESR
lesr = 0.01; %Filter inductor ESR

%% Error amplifier and compensation components
cp = (220+470)*p; %HF roll-off parallel to r-c P-Z pair
%cp = (20)*p; %HF roll-off parallel to r-c P-Z pair
cf = 10*n; %Low frequency pole
%cf = 22*n; %Low frequency pole
rf = 69*k; %Forms Zero with cs
%rf = 422*k; %Forms Zero with cs
ri = 22*k; %Input feed resistor 
ro = 1*k;  %Resistor in series with optocoupler LED
ctr = 0.5;  %Optocoupler CTR
fc_opto = 8*k; %Optocoupler cut-of frequency (pole frequency)

%% Error amplifier transfer function 
p0 = 1./(s.*ri*cp*ro);
p1 = (cp + cf)./(rf*cp*cf);
z0 = 1/(rf*cf);
p_opt = 1/(2*pi*fc_opto);
H_EA = -(p0).*(s + z0)./(s + p1); %Without "fast lane"
H_LED = 1/ro - H_EA;  %Add "fast lane" effect
H_comp = Rfeed*gipk*H_LED*ctr./(s*p_opt+1);

%Then the stupidity pole
cstupid = 47*n;
rstupid = 499;
rpole_stupid = 499+407;
H_stupid = (s.*(2*pi*rstupid*cstupid) + 1)./(s.*(2*pi*rpole_stupid*cstupid) + 1);

%% Slope compensation required for <6dB valley current peaking 
mcmp=(3*vout*Nps-vin_min)/(4*L)

wm=2*pi*fsw;
w=0;
nfs=1;
w=(1:1:nfs*wm);
s=j*w;
z=e.^(-s*Tsw);

%% Computed system parameters
idg = iout/Nps;
vdg=vout*Nps;
vcg=vin-2;
D=vdg/(vcg+vdg)
Dp = 1-D;
mc=vcg/L;
md=vdg/L;

alpha = (mc+md) / (mc + mcmp);

hz = alpha./(1- (1-alpha)*z);

Iv = idg*(vcg+vdg)/vcg - (Tsw/(2*L))*vcg*vdg/(vcg+vdg)
hdg = (Iv/(mc+md)).*(mc/Iv-s);

gDG = 2/(Dp^2*Tsw^2*md + 2*Dp*Tsw*Iv);
HDG = gDG*(Iv+md*Dp*Tsw).*((1 - e.^(-s*Dp*Tsw))./s).*e.^(-s*D*Tsw) - gDG*md*((1 - (1+s*Dp*Tsw).*e.^(-s*Dp*Tsw))./(s.^2)).*e.^(-s*D*Tsw);

%% Output impedance network
rout = vout/idg;
zlf = s*lf + lesr;
zcl = 1./(s*cload) + cesr;
zcout = 1./(s*cout) + cesr/ncout;
zl = zlf+zcl*rout./(rout+zcl);
zout = zl.*zcout./(zcout+zl);

subplot(3,1,1)
semilogx(w,20*log10(abs(H_stupid.*H_comp.*HDG.*hdg.*hz.*zout)))
%semilogx(w,20*log10(abs(H_stupid)))
%semilogx(w,20*log10(abs(H_comp)))
%semilogx(w,20*log10(abs(HDG)))
%semilogx(w,20*log10(abs(zout)))
subplot(3,1,2)
phase = unwrap(angle(-H_stupid.*H_comp.*HDG.*hdg.*hz.*zout));
semilogx(w,180*phase/pi)
%semilogx(w,180*(unwrap(angle(HDG)))/pi)
subplot(3,1,3)

%phase = unwrap(angle(HDG));
lp=length(phase);
lp1 = lp-1;
p1 = phase(1:lp1);
p0 = phase(2:lp);
dp = p1 - p0;
wp = w(1:lp1);
semilogx(wp,dp)

gd = 1e6*dp(392698)
fx = 1e6/gd
