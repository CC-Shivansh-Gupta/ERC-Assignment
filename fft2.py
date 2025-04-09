import numpy as np
from scipy import signal
from scipy.io import wavfile
import os
import glob

import matplotlib.pyplot as plt

def load_audio(file_path):
    sample_rate, audio_data = wavfile.read(file_path)
    if audio_data.dtype.kind == 'i':
        audio_data = audio_data.astype(float) / np.iinfo(audio_data.dtype).max
    
    # If stereo, convert to mono by averaging channels
    if len(audio_data.shape) > 1:
        audio_data = np.mean(audio_data, axis=1)
    
    return sample_rate, audio_data

def analyze_spectrum(signal_data, sample_rate, title="Frequency Spectrum"):
    n = len(signal_data)
    frequencies = np.fft.rfftfreq(n, 1/sample_rate)
    signal_fft = np.fft.rfft(signal_data)
    magnitudes = np.abs(signal_fft)
    
    plt.figure(figsize=(12, 6))
    plt.plot(frequencies, magnitudes)
    plt.title(title)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude')
    plt.grid(True)
    plt.xlim(0, min(20000, sample_rate/2))  # Display up to 20kHz or Nyquist frequency
    plt.tight_layout()
    
    return frequencies, magnitudes

def find_carrier_frequency(frequencies, magnitudes):
    # Exclude DC component and very low frequencies
    start_idx = np.argmax(frequencies > 1000)  # Start search from 1 kHz
    peak_idx = np.argmax(magnitudes[start_idx:]) + start_idx
    carrier_freq = frequencies[peak_idx]
    
    print(f"Carrier frequency detected at: {carrier_freq:.2f} Hz")
    
    # Mark the carrier frequency in the plot
    plt.figure(figsize=(12, 6))
    plt.plot(frequencies, magnitudes)
    plt.axvline(x=carrier_freq, color='r', linestyle='--')
    plt.title(f"Frequency Spectrum with Carrier at {carrier_freq:.2f} Hz")
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude')
    plt.grid(True)
    plt.xlim(0, min(20000, frequencies[-1]))
    plt.tight_layout()
    
    return carrier_freq

def demodulate_am(signal_data, sample_rate, carrier_freq):
    # Create time array
    t = np.arange(len(signal_data)) / sample_rate
    
    # Create carrier signal
    carrier = np.cos(2 * np.pi * carrier_freq * t)
    
    # Demodulate by multiplying with carrier
    demodulated = signal_data * carrier
    
    # Plot demodulation steps
    plt.figure(figsize=(12, 10))
    
    plt.subplot(3, 1, 1)
    plt.plot(t[:1000], signal_data[:1000])
    plt.title('Modulated Signal (First 1000 samples)')
    plt.grid(True)
    
    plt.subplot(3, 1, 2)
    plt.plot(t[:1000], carrier[:1000])
    plt.title(f'Carrier Signal at {carrier_freq:.2f} Hz (First 1000 samples)')
    plt.grid(True)
    
    plt.subplot(3, 1, 3)
    plt.plot(t[:1000], demodulated[:1000])
    plt.title('Demodulated Signal (First 1000 samples)')
    plt.grid(True)
    
    plt.tight_layout()
    
    return demodulated

def apply_bandpass_filter(signal_data, sample_rate, lowcut, highcut, order=5):
    nyquist = 0.5 * sample_rate
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = signal.butter(order, [low, high], btype='band')
    filtered_signal = signal.filtfilt(b, a, signal_data)
    
    # Plot filter response
    w, h = signal.freqz(b, a, worN=2000)
    plt.figure(figsize=(10, 5))
    plt.plot((sample_rate * 0.5 / np.pi) * w, abs(h))
    plt.title('Bandpass Filter Frequency Response')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Gain')
    plt.grid(True)
    plt.axvline(lowcut, color='r', linestyle='--')
    plt.axvline(highcut, color='r', linestyle='--')
    plt.xlim(0, min(20000, sample_rate/2))
    plt.tight_layout()
    
    return filtered_signal

def compare_signals(original, filtered, sample_rate, title="Original vs Filtered Signal"):
    t = np.arange(len(original)) / sample_rate
    
    # Time domain comparison
    plt.figure(figsize=(12, 8))
    
    plt.subplot(2, 1, 1)
    plt.plot(t[:1000], original[:1000])
    plt.title('Original Signal (First 1000 samples)')
    plt.grid(True)
    
    plt.subplot(2, 1, 2)
    plt.plot(t[:1000], filtered[:1000])
    plt.title('Filtered Signal (First 1000 samples)')
    plt.grid(True)
    
    plt.tight_layout()
    
    # Frequency domain comparison
    analyze_spectrum(original, sample_rate, "Original Signal Spectrum")
    analyze_spectrum(filtered, sample_rate, "Filtered Signal Spectrum")

def save_audio(signal_data, sample_rate, file_path):
    # Normalize to avoid clipping
    normalized_signal = signal_data / np.max(np.abs(signal_data))
    wavfile.write(file_path, sample_rate, (normalized_signal * 32767).astype(np.int16))
    print(f"Audio saved to: {file_path}")

def main():
    # Step 1: Find and load the modulated audio file
    print("Looking for modulated audio file...")

    file_path = "signal_modulated_noisy_audio.wav"
    print(f"Using file: {file_path}")
    
    # Load the audio data
    sample_rate, audio_data = load_audio(file_path)
    print(f"Audio loaded: {len(audio_data)} samples at {sample_rate} Hz")
    
    # Step 2: Analyze the modulated signal using FFT
    print("Analyzing frequency spectrum...")
    frequencies, magnitudes = analyze_spectrum(audio_data, sample_rate, "Modulated Signal Spectrum")
    
    # Step 3: Find the carrier frequency
    carrier_freq = find_carrier_frequency(frequencies, magnitudes)
    
    # Step 4: Demodulate the signal
    print("Demodulating signal...")
    demodulated_signal = demodulate_am(audio_data, sample_rate, carrier_freq)
    
    # Step 5: Analyze the demodulated signal
    analyze_spectrum(demodulated_signal, sample_rate, "Demodulated Signal Spectrum")
    
    # Step 6: Apply bandpass filter
    print("Applying bandpass filter...")
    # Typical values for audio: speech (300-3400 Hz), music (20-20000 Hz)
    lowcut = 20   # Lower cutoff frequency in Hz
    highcut = 6000  # Upper cutoff frequency in Hz
    filtered_signal = apply_bandpass_filter(demodulated_signal, sample_rate, lowcut, highcut)
    
    
    # Step 7: Compare the original and filtered signals
    print("Comparing signals...")
    compare_signals(demodulated_signal, filtered_signal, sample_rate)
    
    # Step 8: Save the filtered audio
    output_file = "filtered_audio.wav"
    save_audio(filtered_signal, sample_rate, output_file)
    
    print("Processing complete!")
    plt.show()

if __name__ == "__main__":
    main()
