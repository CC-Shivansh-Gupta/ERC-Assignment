For this question we were supposed to filter a noisy amplitude modulated audio. 
Amplitude Modulation is when you put your wave on a new carrier wave wtih high frequency that helps in transmitting it long distances.
so the equation becomes (A + m(t))cos(wt).
To solve this we first perform a fourier transform that breaks down the signal into comprising sine wave frequencies that are visible as a peak in the frequency and the intesity graph obtained after the fft is performed. 
we first take in input of the file and get the sample rate (that helps define the max freq it can store) and the audio data. Stereo is converted to mono by averaging.
We normalise the data for effective handling and analysis of the data.
then we analyse the spectrum using fft and see what the frequencies are.
as carrier freq is supposed to be of high freq we filter out the highest frequency fromt the data obtained.
![image](https://github.com/user-attachments/assets/ccd5da6c-d94a-4120-819b-a46b9bee6eac)
![image](https://github.com/user-attachments/assets/3aa5673f-425e-406a-b030-e61ed5ac61a2)
so we demodulate the signal by removing the carrier frequecy. it is done by multiplying the signal with cos(2pifct) that seperates out 1/2m(t) and another component that includes carrier frequency which is a high frequncy component.
![image](https://github.com/user-attachments/assets/bd36bbdf-5213-417a-8564-85ebe24709fc)
![image](https://github.com/user-attachments/assets/25ae0413-c77c-4563-9aea-5ce3be81d558)
next we apply a low pass digital filter that lets low frequencies pass and blocks high frequency signals.
![image](https://github.com/user-attachments/assets/cfe84c89-984f-4521-8c1b-8ce7e03ef1cd)
![image](https://github.com/user-attachments/assets/f280424d-65db-401b-b3c6-b3ad77d716d0)
then we compare the signals and save them to a new file
![image](https://github.com/user-attachments/assets/0e54fcb7-4b17-49cf-88ae-d5882814b0b8)
