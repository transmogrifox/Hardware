k = 1000;
u = 1e-6;

fsw = 100*k
Ts = 1/fsw;

ff = 100:10:fsw;
ws = 2*pi*ff;
s = j*ws;
z1 = e.^(-s*Ts);

# Gain at Fsw/2 algebraic manipulation
# Gpk = alpha/(2-alpha)
# 2*Gpk - alpha*Gpk = alpha
# 2*Gpk = alpha*(1 + Gpk)
# alpha = 2*Gpk/(1 + Gpk)
# Gpk = 10^(GpkdB/20)

alpha = 1.0;
GdB = -9  # Peak gain in dB at Fsw/2

hold on
for i = 1:1:7
  Gpk = 10^(GdB/20);
  alpha = 2*Gpk/(1 + Gpk)  
##
## Transfer Function:
## Peak current mode controller
##
  hz = alpha*z1./(1-(1-alpha)*z1);
##
##
  semilogx(ff, 20*log10(abs(hz)))  
  GdB = GdB + 3; #Post-increment to continue set of traces
endfor  

semilogx(ff, 20*log10(abs(hz)))
#title("Peak Current Mode Controller system response with varying amounts of slope compensation")
xlabel("Frequency (Hz)")
ylabel("Magnitude (dB)")

text(135000, 9, "ɑ = 1.476")
text(135000, 6, "ɑ = 1.332")
text(135000, 3, "ɑ = 1.171")
text(135000, 0, "ɑ = 1.00")
text(135000, -3, "ɑ = 0.829")
text(135000, -6, "ɑ = 0.668")
text(135000, -9, "ɑ = 0.524")
