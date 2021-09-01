import librosa, random, math, numpy, soundfile, sys

class AddNoise:
    verbose = False
    noiseSource = None
    def __init__(self, verbose = False, noise_file = None):
        self.verbose = verbose
        if noise_file:
            self.noiseSource, sr2 = librosa.load(noise_file)
            self.noiseSource = numpy.interp(self.noiseSource,
                (self.noiseSource.min(), self.noiseSource.max()), (-1, 1))   

    def addNoiseFromFile(self, file, fileWithNoise, SNR):
        if self.verbose:
            print('adding noise to file:', file)

        signal, sr = librosa.load(file)    
        signal = numpy.interp(signal, (signal.min(), signal.max()), (-1, 1)) 
        
        startCut = random.randrange(0, len(self.noiseSource)-len(signal))
        noise = self.noiseSource[startCut:startCut + len(signal)]
        
        RMS_s = math.sqrt(numpy.mean(signal**2))        
        RMS_n = math.sqrt(RMS_s**2/(pow(10, SNR/10)))        
        RMS_n_current = math.sqrt(numpy.mean(noise**2))
        noise = noise*(RMS_n/RMS_n_current)
        
        signal_n = signal + noise

        if self.verbose:
            print('write modified file:', fileWithNoise)
        soundfile.write(fileWithNoise, signal_n, sr)

    def addWhiteNoise(self, file, fileWithNoise, SNR):
        if self.verbose:
            print('adding noise to file:', file)

        signal, sr = librosa.load(file)
        
        RMS_s=math.sqrt(numpy.mean(signal**2))    
        RMS_n=math.sqrt(RMS_s**2/(pow(10, SNR/10)))
        noise = numpy.random.normal(0, RMS_n, signal.shape[0])

        signal_n = signal + noise

        if self.verbose:
            print('write modified file:', fileWithNoise )
        soundfile.write(fileWithNoise, signal_n, sr)

if __name__ == "__main__":
    nArgs = len(sys.argv)
    
    inputFile = sys.argv[1]
    outputFile = sys.argv[2]
    snr = int(sys.argv[3])
    
    noiseFile = sys.argv[4] if nArgs>4 else None
    
    #0 white noise, 1 noise file
    mode = int(sys.argv[5]) if nArgs>5 else 0
    
    verbose = int(sys.argv[6]) if nArgs>6 else 0

    an = AddNoise(verbose, noiseFile)
    if mode==0:
        an.addWhiteNoise(inputFile, outputFile, snr)
    elif mode==1:
    	an.addNoiseFromFile(inputFile, outputFile, snr)
