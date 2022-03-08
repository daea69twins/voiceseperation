[x,Fs] = audioread('PlaneWspeech.wav');
%Fsf= 20e3;     %sampling frequency 
%Fp= 1000;        %Passband frequency in Hz 
%Fst = 300;  % stopband frequency 
%Ap = 0.5;     %passbandribble in db
%Ast = 75; %stopband attenuation
C1 = 150;
C2 = 3200;

df = designfilt('bandpassiir', 'FilterOrder',20, 'HalfPowerFrequency1' , C1, 'HalfPowerFrequency2', C2, 'sampleRate', Fs);
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