[y,fs]=audioread('PlaneWspeech.wav');
t=linspace(0,length(y)/fs,length(y));
plot(t,y);
Nfft=1024;
f=linspace(0,fs,Nfft);
G=abs(fft(y,Nfft));
figure ; plot(f(1:Nfft/2),G(1:Nfft/2));

o = 3;
wn = [250 2500]*2/fs;
[b,a] = butter(o,wn,'bandpass');
figure; freqz(b,a,1024,fs);
z_filt = filter(b,a,G);
plot(f,z_filt);
