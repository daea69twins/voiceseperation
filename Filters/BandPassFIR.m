[x,Fs] = audioread('PlaneWspeech.wav');
Fstop1 = 100;
Fpass1 = 300;
Fpass2 = 2000;
Fstop2 = 2100;
Astop1 = 45;
Apass  = 0.5;
Astop2 = 45;
%Fs = 1e3;


%d = designfilt('bandpassfir', 'StopbandFrequency1', Fstop1, 'PassbandFrequency1', Fpass1, 'PassbandFrequency2', Fpass2, 'StopbandFrequency2', Fstop2, 'StopbandAttenuation1', Astop1, 'PassbandRipple', Apass, 'StopbandAttenuation', Astop2, 'DesignMethod', 'equiripple', 'SampleRate', Fs);
d = designfilt('bandpassfir', 'StopbandFrequency1', Fstop1, ...
               'PassbandFrequency1', Fpass1, 'PassbandFrequency2', ...
               Fpass2, 'StopbandFrequency2', Fstop2, ...
               'StopbandAttenuation1', Astop1, 'PassbandRipple', Apass, ...
               'StopbandAttenuation2', 60, 'SampleRate', 48000, ...
               'DesignMethod', 'equiripple');
fvtool(d)

y = filter(d, x);

subplot(3,1,1)
plot(x)
title('original signal')
%subplot(3,1,2)
%plot(xn)
%title('Noisy signal')
subplot(3,1,2)
plot(y)
title('filtered signal')
pause();

