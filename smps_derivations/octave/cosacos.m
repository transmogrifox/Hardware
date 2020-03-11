x=2*pi*(1:1:1000)/1000;

fc = cos(x);
fa = abs(acos(x));
fg = acos(x);
fg(1)
2*acos(0)/pi

plot(x,fc, x,fa)