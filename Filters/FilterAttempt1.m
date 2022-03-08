% TRYING TO SEPARATE VOICE AND BACKGROUND MUSIC
% TAKING AN AUDIO FILE IN .WAVFORMAT
 
[y,fs] = audioread('test2.wav');
 
%ALLIGNING THE VALUES TO LENGTH OF AUDIO, AND DF IS THE MINIMUM FREQUENCY RANGE
length_audio = length(y);
df = fs/length_audio;
 
%CALCULATING FREQUENCY VALUES TO BE ASSIGNED ON THE X-AXIS OF THE GRAPH
frequency_audio = -fs/2:df:fs/2-df;
 
%BY APPLYING FOURIER TRANSFORM TO THE AUDIO FILE
FFT_audio_in = fftshift(fft(y)/length(fft(y)));
 
% PLOTTING
%plot(frequency_audio,abs(FFT_audio_in));
plot(FFT_audio_in,abs(frequency_audio));
title('FFT of input Audio');
xlabel('frequency(HZ)');
ylabel('Amplitude');
 
%NOW LETS SEPARATE THE VARIOUS COMPONENTS BY CUTTING IT IN FREQUENCY RANGE
lower_threshold = 150;
upper_threshold = 2500;
 
% WHEN THE VALUES IN THE ARRAY ARE IN THE FREQUENCY RANGE THEN WE HAVE 1 AT
% THAT INDEX AND O FOR OTHERS I.E; CREATING AN BOOLEAN INDEX ARRAY
 
val = abs(frequency_audio)<upper_threshold & abs(frequency_audio)>lower_threshold;
FFT_ins = FFT_audio_in(:,1);
FFT_voc = FFT_audio_in(:,1);
%BY THE LOGICAL ARRAY THE FOURIER IN FREQUENCY RANGE IS KEPT IN VOCALS;AND
%REST IN INSTRUMENTAL AND REST OF THE VALUES TO ZERO
FFT_ins(val) = 0;
FFT_voc(~val) = 0;
 
%NOW WE PERFORM THE INVERSE FOURIER TRANSFORM TO GET BACK THE SIGNAL
FFT_a = ifftshift(FFT_audio_in);
FFT_a11 = ifftshift(FFT_ins);
FFT_a31 = ifftshift(FFT_voc);
 
%CREATING THE TIME DOMAIN SIGNAL
s1 = ifft(FFT_a11*length(fft(y)));  
s3 = ifft(FFT_a31*length(fft(y)));
 
%WRITING THE FILE
audiowrite('sound_background.wav',s1,fs);
audiowrite('sound_voice.wav',s3,fs);% TRYING TO SEPARATE VOICE AND BACKGROUND MUSIC
% TAKING AN AUDIO FILE IN .WAVFORMAT
[speech,fs]=audioread('speech.wav');
[music,fs]=audioread('strings.wav');
y=speech(1:length(music),1)+music(:,1);
fs=fs;
[y,fs] = audioread('sound.wav');
 
%ALLIGNING THE VALUES TO LENGTH OF AUDIO, AND DF IS THE MINIMUM FREQUENCY RANGE
length_audio = length(y);
df = fs/length_audio;
 
%CALCULATING FREQUENCY VALUES TO BE ASSIGNED ON THE X-AXIS OF THE GRAPH
frequency_audio = -fs/2:df:fs/2-df;
 
%BY APPLYING FOURIER TRANSFORM TO THE AUDIO FILE
FFT_audio_in = fftshift(fft(y)/length(fft(y)));
music_audio_in = fftshift(fft(music)/length(fft(music)));
speech_audio_in = fftshift(fft(speech(1:length(music),1))/length(fft(speech(1:length(music),1))));
% PLOTTING
%plot(frequency_audio,abs(FFT_audio_in));
plot(frequency_audio,abs(music_audio_in));
title('FFT of input Audio');
xlabel('frequency(HZ)');
ylabel('Amplitude');
 
%NOW LETS SEPARATE THE VARIOUS COMPONENTS BY CUTTING IT IN FREQUENCY RANGE
lower_threshold = 970000;
upper_threshold = 2630000;
 
% WHEN THE VALUES IN THE ARRAY ARE IN THE FREQUENCY RANGE THEN WE HAVE 1 AT
% THAT INDEX AND O FOR OTHERS I.E; CREATING AN BOOLEAN INDEX ARRAY
 
val = abs(frequency_audio)<upper_threshold & abs(frequency_audio)>lower_threshold;
FFT_ins = FFT_audio_in(:,1);
FFT_voc = FFT_audio_in(:,1);
%BY THE LOGICAL ARRAY THE FOURIER IN FREQUENCY RANGE IS KEPT IN VOCALS;AND
%REST IN INSTRUMENTAL AND REST OF THE VALUES TO ZERO
FFT_ins(val) = 0;
FFT_voc(~val) = 0;
 
%NOW WE PERFORM THE INVERSE FOURIER TRANSFORM TO GET BACK THE SIGNAL
FFT_a = ifftshift(FFT_audio_in);
FFT_a11 = ifftshift(FFT_ins);
FFT_a31 = ifftshift(FFT_voc);
 
%CREATING THE TIME DOMAIN SIGNAL
s1 = ifft(FFT_a11*length(fft(y)));  
s3 = ifft(FFT_a31*length(fft(y)));
 
%WRITING THE FILE
audiowrite('sound_background.wav',s1,fs);
audiowrite('sound_voice.wav',s3,fs);