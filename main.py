import os
from argparse import ArgumentParser, Namespace

import numpy as np
# import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import welch
import ffmpeg

def mesure_cutoff_frequency(wav_file):
    # Read sample data from file
    sample_rate, sample_data = wavfile.read(wav_file)

    # Convert data to mono if file is stereo
    if len(sample_data.shape) == 2:
        sample_data = np.mean(sample_data, axis=1)

    # Calculate Power Spectral Density (PSD)
    frequencies, psd = welch(sample_data, sample_rate, nperseg=2048) # nperseg determine "precision" 2048 is a good compromise of time/precision

    lowest_psd_index = np.argmin(psd)
    if psd[lowest_psd_index] > 0.01:
        cutoff_frequency = sample_rate/2
    else:
        low_psd_index = np.where(psd < 0.5)
        cutoff_frequency = frequencies[low_psd_index][0]

    np.savetxt('freqs2.txt', frequencies, fmt='%4.6f', delimiter=' ')
    np.savetxt('psd2.txt', psd, fmt='%4.6f', delimiter=' ')


    # # Visualiser le spectre
    # plt.figure(figsize=(12, 6))
    # plt.semilogy(frequencies, psd)
    # plt.axvline(x=cutoff_frequency, color='r', linestyle='--', label=f'Cutoff Frequency: {cutoff_frequency:.2f} Hz')
    # plt.title("Spectre de puissance du signal")
    # plt.xlabel("Fréquence (Hz)")
    # plt.ylabel("Densité spectrale de puissance")
    # plt.legend()
    # plt.grid(True)
    # plt.show()

    return cutoff_frequency

def main(file_path):
    audio_path = os.path.join(PWD, "temp.wav")
    try:
        (
            ffmpeg
            .input(file_path)
            .output(audio_path)
            .overwrite_output()
            .run()
        )
    except Exception as e:
        print(e)
    
    cutoff_frequency = mesure_cutoff_frequency(audio_path)
    os.remove(audio_path)
    return cutoff_frequency
    
    

PWD = os.getcwd()

CUTOFF_BITRATE_MP3 = {
    22050: "lossless ",
    20000: 320,
    19500: "256 (or 224)",
    18500: 192,
    17500: 160,
    16500: 128,
    15500: 112,
    15000: 96,
    13000: 80,
    11000: 64,
    10500: 56,
    8000: 48,
    7000: 40,
    6000: 32,
}

if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument("path", help="Video or audio file path")

    args: Namespace = parser.parse_args()

    cutoff_frequency = main(args.path)

    closest_frequency = min(CUTOFF_BITRATE_MP3, key=lambda x:abs(x-cutoff_frequency))
    print(f"Cutoff frequency : {cutoff_frequency}Hz")
    print(f"The determined bitrate is : {CUTOFF_BITRATE_MP3[closest_frequency]}kbps")
    print("Note that the data used for determining the bitrate was measure in sub-optimal environment and would not be an accurate representation of the true bitrate of the audio, only an aproximative bitrate")
