u=1e-6;
k=1e3;

%% Flyback converter open loop gain
fsw=125*k; %Switching frequency
Nps = 54/8; %Transformer Primary-Secondary turns ratio
L=580*u; %Primary inductance
vin = 88; %Input voltage
vin_min = 75; %Minimum input voltage
vout = 12; %Output voltage
iout = 3; %Output current

%% Slope compensation required for <6dB valley current peaking 
mcmp=(3*vout*Nps-vin_min)/(4*L)

wm=2*pi*fsw;
w=0;
w=(1:1:1*wm);
s=j*w;
z=e.^(-s*Tsw);

%% Computed system parameters
Tsw = 1/fsw;
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

cout = 4*470*u;
rout = vout/idg;
zout = rout./(s*rout*cout + 1);

subplot(2,1,1)
semilogx(w,20*log10(abs(HDG.*hdg.*hz.*zout)))
%semilogx(w,20*log10(abs(HDG)))
subplot(2,1,2)
semilogx(w,180*(unwrap(angle(HDG.*hdg.*hz.*zout)))/pi)
%semilogx(w,180*(unwrap(angle(HDG)))/pi)