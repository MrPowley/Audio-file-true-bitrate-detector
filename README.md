# Audio-file-true-bitrate-detector

It depends on the codec used, but in general, the frequency range of an audio file will be determined by its bitrate, so for example, with an mp3, if the file bitrate is set as 64kbps, the frequencies will cut above around 11.2kHz
![64kbps spectrogram](https://github.com/MrPowley/Audio-file-true-bitrate-detector/blob/main/Images/64kbps-mp3.png?raw=true)

wheras a 128kbps file will cutoff at around 16kHz.
![64kbps spectrogram](https://github.com/MrPowley/Audio-file-true-bitrate-detector/blob/main/Images/128kbps-mp3.png?raw=true)

Using this, the program measures at what frequency the sound is no longer audible (no longer present) and uses an imprecise chart to determine the bitrate.
Note that it doesn't work for lossless audio because the base of lossless is to not have any loss in data, so the largest frequency range possible, and thus there is no cutoff.
With this method, we can't be fooled by incorrect metadata and get the true bitrate