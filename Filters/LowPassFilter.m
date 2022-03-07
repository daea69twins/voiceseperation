close all; clear all;
[x,Fs] = audioread('test2.wav');
%Fsf= 20e3;     %sampling frequency 
Fp= 800;        %Passband frequency in Hz 
Fst = 1200;  % stopband frequency 
Ap = 2;     %passbandribble in db
Ast = 95; %stopband attenuation

df = designfilt('lowpassfir', 'PassbandFrequency', Fp, 'StopbandFrequency',Fst, 'passbandRipple', Ap, 'stopbandAttenuation', Ast, 'sampleRate', Fs);
fvtool(df); % visualize freq response of filter
%xn = awgn(x,0,'measured'); % signal corrupted by white Gaussian noise
y = filter(df, x);
%plotting signals

subplot(3,1,1)
plot(x)
title('original signal')
%subplot(3,1,2)
%plot(xn)
%title('Noisy signal')
subplot(3,1,2)
plot(y)
title('filtered signal')