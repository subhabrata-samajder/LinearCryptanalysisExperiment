import SmallPresent as SP

import LinearCryptanalysis as LC

import sys, getopt

import os

import numpy as np
from numpy import random

import math

import scipy.special
import scipy.stats as stats
from scipy.stats import randint

import matplotlib
import matplotlib.pyplot as plot

import seaborn

from mpmath import mp


def main(argv):
    mp.dps = 100
   
    try:
        opts, args = getopt.getopt(argv[1:],"hs:i:",["--help", "--sampling", "--input"])
    except getopt.GetoptError:
        print('Error: %s -s <Sampling Choice> -i <Value of n> <Value of N> <Value of S>' %argv[0])
        sys.exit(2)
    
    for opt, arg in opts:
        if opt in ('-h', "--help"):
            print('Usage: %s -s <Sampling Choice> -i <Value of n> <Value of N> <Value of S>' %argv[0])
            sys.exit()
        elif opt in ("-s", "--sampling"):
            PlaintextSampleChoice = int(arg)
            if (PlaintextSampleChoice < 1) or (PlaintextSampleChoice > 2):
                print("ERROR: PlaintextSampleChoice can take value 1 and 2!\n1: Sample plaintexts using AES in CTR mode\n2: Sample plaintexts using RC4")
                sys.exit(2)
        elif opt in ("-i", "--input"):
            n = int(arg)
            if (n <= 5):
                print("ERROR: n must be greater than 5!")
                sys.exit(2)

            if (n % 4 != 0):
                print("INPUT ERROR: n must be a multiple of 4!")
                sys.exit(2)

    Count = 0
    for arg in args:
        if (arg == ''):
            print('Values of N and S are missing!\nUsage: %s -s <Sampling Choice> -i <Value of n> <Value of N> <Value of S>' %argv[0])
            sys.exit(2)
        elif (Count == 0):
            N = int(arg)
            Count += 1
            if (N > 2**n):
                print("ERROR: N must be less than 2**n")
                sys.exit(2)
        elif (Count == 1):
            S = int(arg)
            Count += 1
        else:
            print("Error: The program takes exactly 3 integer arguments!")

    # To detect the backend used by the machine
    Backend = matplotlib.get_backend()
    if (Backend == 'QT'):
        # For QT backend
        Manager = plot.get_current_fig_manager()
        Manager.window.showMaximized()
    elif (Backend == 'TkAgg'):
        # TkAgg backend
        Manager = plot.get_current_fig_manager()
        Manager.resize(*Manager.window.maxsize())
    elif (Backend == 'WX'):
        # WX backend
        Manager = plot.get_current_fig_manager()
        Manager.frame.Maximize(True)

    # Initializing the parameters of Small Present
    Nibbles = int(n/4)
    Rounds = 10
    KeyLen = 80

    # Choosing the correct key
    Key = 0
    for i in range(int(KeyLen/4)):
        Key ^= (int(np.random.randint(0, 16, size = 1)[0]) << (4*i))

    # Generating Round keys
    Sbox = [12, 5, 6, 11, 9, 0, 10, 13, 3, 14, 15, 8, 4, 7, 1, 2]

    RoundKeys = SP.GenerateRoundKeys(Key, KeyLen, Nibbles, Rounds, Sbox)

    # Randomly selecting the input and output masks, along with the number of target subkey bits m, 
    # the (r + 1)-round target subkey bits and the rth round target subkey bits
    InputMask, OutputMask, m, SubKeyNibblesR = LC.FindMasksSubKey(Nibbles)

    # Guessing the rth round and (r + 1)th round subkey bits
    KeyGuessR, KeyGuessR1 = LC.KeyGuess(m, Rounds, RoundKeys, SubKeyNibblesR)

    RawSample = [0 for i in range(N + 1)]
    for i in range(S):
        Count = LC.LinearCryptanalysis(PlaintextSampleChoice, Nibbles, Rounds, KeyLen, RoundKeys, InputMask, OutputMask, m, SubKeyNibblesR, N, KeyGuessR, KeyGuessR1)
        
        RawSample[Count] += 1

        if (i == int(S/4)):
            print("%s iterations Completed!" %(int(S/4)))
        elif (i == int(S/2)):
            print("%s iterations Completed!" %(int(S/2)))
        elif (i == (3*int(S/4))):
            print("%s iterations Completed!" %(3*int(S/4)))
    print("Sample generation completed!")

    # Calculating the empirical distribution, sample mean and sample variance
    Temp = [0 for i in range(N + 1)]
    SampleMean = 0
    SampleVar = 0
    for i in range(N + 1):
        SampleMean += i*RawSample[i]
        SampleVar += i*i*RawSample[i]
        Temp[i] = RawSample[i]/S

    SampleMean = SampleMean/S
    SampleVar = (SampleVar/S) - (SampleMean*SampleMean)

    # To save the RawSample in a file. First Checks whether the directories n%s, n%s/% Rounds, n%s/%s Rounds/Data exists or not. If not then it cr-
    # eates these directories. It then checks if the file named n%s-N%s-S%s.txt exists or not. If yes then goes on checking for i for  which the f-
    # ile n%s-N%s-S%s_i.txt does not exits. It then creates the file named n%s-N%s-S%s_i.txt.
    Dir = os.path.isdir('./n%s' %(n))
    if (Dir == False):
        os.mkdir('./n%s' %(n))

    Dir = os.path.isdir('./n%s/%s Rounds' %(n, Rounds))
    if (Dir == False):
        os.mkdir('./n%s/%s Rounds' %(n, Rounds))

    # Printing Raw Data in a file 
    Dir = os.path.isdir('./n%s/%s Rounds/Data' %(n, Rounds))
    if (Dir == False):
        os.mkdir('./n%s/%s Rounds/Data' %(n, Rounds))

    File = os.path.isfile("./n%s/%s Rounds/Data/n%s-N%s-S%s.txt" %(n, Rounds, n, N, S))
    if (File == True):
        Counter = 0
        while(File == True):
            Counter += 1
            File = os.path.isfile("./n%s/%s Rounds/Data/n%s-N%s-S%s_%s.txt" %(n, Rounds, n, N, S, Counter))

        File = open("./n%s/%s Rounds/Data/n%s-N%s-S%s_%s.txt" %(n, Rounds, n, N, S, Counter), 'w')
    else:
        File = open("./n%s/%s Rounds/Data/n%s-N%s-S%s.txt" %(n, Rounds, n, N, S), 'w')
    
    print("n = %s, N = %s, S = %s, m = %s, Rounds = %s\nSample Mean = %s, Sample Variance = %s" %(n, N, S, 8*m, Rounds, SampleMean, SampleVar), file = File)
    print("Correct Key = %s, Input Mask = %s, Output Mask = %s" %(hex(Key), hex(InputMask), hex(OutputMask)), file = File)
    print("Last Round Key Guess = %s, Last But One Round Key Guess = %s" %(hex(KeyGuessR1), hex(KeyGuessR)), file = File)
    print("RawSample = %s" %(RawSample), file = File)

    File.close()

    # RawSample sample now holds the empirical distribution
    RawSample = Temp

    # Generating empirical distribution over 3*sigma range about the N/2.
    ThreeSigma = int(mp.floor(3*mp.sqrt(N/4)))                                              # For taking 3*sigma interval around the mean N/2

    Sample = [0 for i in range(int(N/2) - ThreeSigma, int(N/2) + ThreeSigma + 2)]

    for i in range(N + 1):
        if (i <= int(N/2) - ThreeSigma):
            Sample[0] += RawSample[i]
        elif (i > int(N/2) + ThreeSigma):
            Sample[len(Sample) - 1] += RawSample[i]
        else:
            Sample[i - (int(N/2) - ThreeSigma)] = RawSample[i]

    # Plotting the empirical distribution
    XRange = [i/N for i in range(int(N/2) - ThreeSigma + 1, int(N/2) + ThreeSigma + 1)]
    YRange = Sample[1:len(Sample) - 1]

    plot.plot(XRange, YRange, color='green', marker='o', markerfacecolor='green', markersize=3, label='Empirical Distribution')
    plot.vlines(XRange, 0, YRange, colors='green', lw=1)

    # Calculating the mean and standard deviation of BT distribution
    Mu0 = N/2
    Var0 = (N*(1 + N/2**(n)))/4
    Sigma0 = mp.sqrt(Var0)

    # Calculating the mean and standard deviation of Std distribution
    Mu1 = N/2
    Var1 = N/4
    Sigma1 = mp.sqrt(Var1)

    # Labeling the x and y axes
    plot.xlabel('x')
    plot.ylabel('Probability')

    # Giving a title to plotted graph
    plot.title('Plot of empirical data where n = %s, N = %s, S = %s, m = %s, Rounds = %s, Key Length = %s,\nCorrect Key = %s, Plaintext Mask = %s, Output Mask = %s,\nLast Round Key Guess = %s, Second Last Round Key Guess = %s,\nMean = %s, Variance = %s' %(n, N, S, 8*m, Rounds, KeyLen, hex(Key), hex(InputMask), hex(OutputMask), hex(KeyGuessR1), hex(KeyGuessR), SampleMean, SampleVar))
    
    # To save the RawSample in a file. First Checks whether the directories n%s, n%s/% Rounds, n%s/%s Rounds/Plot exists or not. If not then it cr-
    # eates these directories. It then checks if the file named n%s-N%s-S%s.pdf exists or not. If yes then goes on checking for i for  which the f-
    # ile n%s-N%s-S%s_i.pdf does not exits. It then creates the file named n%s-N%s-S%s_i.pdf.
    Dir = os.path.isdir('./n%s/%s Rounds/Plots' %(n, Rounds))
    if (Dir == False):
        os.mkdir('./n%s/%s Rounds/Plots' %(n, Rounds))

    File = os.path.isfile("./n%s/%s Rounds/Plots/n%s-N%s-S%s.pdf" %(n, Rounds, n, N, S))
    if (File == True):
        Counter = 0
        while(File == True):
            Counter += 1
            File = os.path.isfile("./n%s/%s Rounds/Plots/n%s-N%s-S%s_%s.pdf" %(n, Rounds, n, N, S, Counter))

        Figure = plot.gcf()                                                                                     # get current figure
        Figure.set_size_inches(16, 9)                                                                           # set figure's size manually to your full screen (32x18)
        plot.savefig("./n%s/%s Rounds/Plots/n%s-N%s-S%s_%s.pdf" %(n, Rounds, n, N, S, Counter), bbox_inches='tight')    # bbox_inches removes extra white spaces
    else:
        Figure = plot.gcf()                                                                                     # get current figure
        Figure.set_size_inches(16, 9)                                                                           # set figure's size manually to your full screen (32x18)
        plot.savefig("./n%s/%s Rounds/Plots/n%s-N%s-S%s.pdf" %(n, Rounds, n, N, S), bbox_inches='tight')        # bbox_inches removes extra white spaces

    return 0

if __name__ == "__main__":
    main(sys.argv[0:])

