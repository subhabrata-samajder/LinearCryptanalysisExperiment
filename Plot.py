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
        opts, args = getopt.getopt(argv[1:],"hi:",["--help", "--input"])
    except getopt.GetoptError:
        print('Error: %s -i <Value of n> <Value of N> <Value of S> <Value of CounterLow> <Value of CounterUpp>' %argv[0])
        sys.exit(2)
    
    for opt, arg in opts:
        if opt in ('-h', "--help"):
            print('Usage: %s -i <Value of n> <Value of N> <Value of S> <Value of CounterLow> <Value of CounterUpp>' %argv[0])
            sys.exit()
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
            print('Values of N and S are missing!\nUsage: %s -s <Sigma Option> <Value of n> <Value of N> <Value of S> <Value of CounterLow> <Value of CounterUpp>' %argv[0])
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
        elif (Count == 2):
            CounterLow = int(arg)
            Count += 1
        elif (Count == 3):
            CounterUpp = int(arg)
            Count += 1

            if (CounterLow > CounterUpp):
                print("Error: 4th argument should be less than or equal to the 5th argument!")
                sys.exit(2)
        else:
            print("Error: The program takes exactly 5 integer arguments!")
            sys.exit(2)

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

    KeyLen = 80
    Rounds = 10

    for Iter in range(CounterLow, CounterUpp + 1):
        plot.clf()

        if (Iter == 0):
            IsFile = os.path.isfile("./n%s/%s Rounds/Data/n%s-N%s-S%s.txt" %(n, Rounds, n, N, S))

            if (IsFile == False):
                print("./n%s/%s Rounds/Data/n%s-N%s-S%s.txt File does not exists!" %(n, Rounds, n, N, S))
                sys.exit(2)

            File = open("./n%s/%s Rounds/Data/n%s-N%s-S%s.txt" %(n, Rounds, n, N, S), "r")
            Buffer = File.read()
            Buffer = Buffer.splitlines()

            m = int(Buffer[0][Buffer[0].find("m = ") + 4: Buffer[0].find(", Rounds")])
        
            Rounds = int(Buffer[0][Buffer[0].find("Rounds = ") + 9: len(Buffer[0])], 10) 

            SampleMean = float(Buffer[1][Buffer[1].find("Sample Mean = ") + 14: Buffer[1].find(", Sample Variance = ")])

            SampleVar = float(Buffer[1][Buffer[1].find("Sample Variance = ") + 18: len(Buffer[1])])

            Key = int(Buffer[2][Buffer[2].find("Correct Key = 0") + 14: Buffer[2].find(", Input Mask = ")], 16)

            InputMask = int(Buffer[2][Buffer[2].find("Input Mask = 0") + 13: Buffer[2].find(", Output Mask = ")], 16)

            OutputMask = int(Buffer[2][Buffer[2].find("Output Mask = 0") + 14: len(Buffer[2])], 16)

            KeyGuessR1 = int(Buffer[3][Buffer[3].find("Last Round Key Guess = 0") + 23: Buffer[3].find(", Last But")], 16)

            KeyGuessR = int(Buffer[3][Buffer[3].find("One Round Key Guess = 0") + 22: len(Buffer[3])], 16)

            RawSample = Buffer[4][Buffer[4].find("RawSample = ") + 13: Buffer[4].find("]")].split(", ")
            for i in range(len(RawSample)):
                RawSample[i] = float(RawSample[i])
        else:
            IsFile = os.path.isfile("./n%s/%s Rounds/Data/n%s-N%s-S%s_%s.txt" %(n, Rounds, n, N, S, Iter))

            if (IsFile == False):
                print("./n%s/%s Rounds/Data/n%s-N%s-S%s_%s.txt File does not exists!" %(n, Rounds, n, N, S, Iter))
                sys.exit(2)

            File = open("./n%s/%s Rounds/Data/n%s-N%s-S%s_%s.txt" %(n, Rounds, n, N, S, Iter), "r")
            Buffer = File.read()
            Buffer = Buffer.splitlines()

            m = int(Buffer[0][Buffer[0].find("m = ") + 4: Buffer[0].find(", Rounds")])
        
            Rounds = int(Buffer[0][Buffer[0].find("Rounds = ") + 9: len(Buffer[0])], 10) 

            SampleMean = float(Buffer[1][Buffer[1].find("Sample Mean = ") + 14: Buffer[1].find(", Sample Variance = ")])

            SampleVar = float(Buffer[1][Buffer[1].find("Sample Variance = ") + 18: len(Buffer[1])])

            Key = int(Buffer[2][Buffer[2].find("Correct Key = 0") + 14: Buffer[2].find(", Input Mask = ")], 16)

            InputMask = int(Buffer[2][Buffer[2].find("Input Mask = 0") + 13: Buffer[2].find(", Output Mask = ")], 16)

            OutputMask = int(Buffer[2][Buffer[2].find("Output Mask = 0") + 14: len(Buffer[2])], 16)

            KeyGuessR1 = int(Buffer[3][Buffer[3].find("Last Round Key Guess = 0") + 23: Buffer[3].find(", Last But")], 16)

            KeyGuessR = int(Buffer[3][Buffer[3].find("One Round Key Guess = 0") + 22: len(Buffer[3])], 16)

            RawSample = Buffer[4][Buffer[4].find("RawSample = ") + 13: Buffer[4].find("]")].split(", ")
            for i in range(len(RawSample)):
                RawSample[i] = float(RawSample[i])

       
        # Graph plotting
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
        plot.title('Plot of empirical data where n = %s, N = %s, S = %s, m = %s, Rounds = %s, Key Length = %s,\nCorrect Key = %s, Plaintext Mask = %s, Output Mask = %s,\nLast Round Key Guess = %s, Last But One Round Key Guess = %s,\nMean = %s, Variance = %s' %(n, N, S, m, Rounds, KeyLen, hex(Key), hex(InputMask), hex(OutputMask), hex(KeyGuessR1), hex(KeyGuessR), SampleMean, SampleVar))
    
        # To save the graph plot in a file. First Checks whether the directory n%s exists or not. If not then it creates a directories n%s. Then checks 
        # if the file named n%sN%sS%s.pdf exists or not. If yes then goes on checking for i for  which the file n%sN%sS%s_i.pdf does not exits. It then 
        # creates the file names n%sN%sS%s_i.pdf.
        Dir = os.path.isdir('./n%s/%s Rounds/Reconstructed' %(n, Rounds))
        if (Dir == False):
            os.mkdir('./n%s/%s Rounds/Reconstructed' %(n, Rounds))

        Dir = os.path.isdir('./n%s/%s Rounds/Reconstructed' %(n, Rounds))
        if (Dir == False):
            os.mkdir('./n%s/%s Rounds/Reconstructed' %(n, Rounds))

        File = os.path.isfile("./n%s/%s Rounds/Reconstructed/n%s-N%s-S%s.pdf" %(n, Rounds, n, N, S))
        if (File == True):
            Counter = 0
            while(File == True):
                Counter += 1
                File = os.path.isfile("./n%s/%s Rounds/Reconstructed/n%s-N%s-S%s_%s.pdf" %(n, Rounds, n, N, S, Counter))

            Figure = plot.gcf()                                                                                 # get current figure
            Figure.set_size_inches(16, 9)                                                                       # set figure's size manually to your full screen (32x18)
            plot.savefig("./n%s/%s Rounds/Reconstructed/n%s-N%s-S%s_%s.pdf" %(n, Rounds, n, N, S, Counter), bbox_inches='tight')    # bbox_inches removes extra white spaces
        else:
            Figure = plot.gcf()                                                                                 # get current figure
            Figure.set_size_inches(16, 9)                                                                       # set figure's size manually to your full screen (32x18)
            plot.savefig("./n%s/%s Rounds/Reconstructed/n%s-N%s-S%s.pdf" %(n, Rounds, n, N, S), bbox_inches='tight')        # bbox_inches removes extra white spaces
    
    return 0

if __name__ == "__main__":
    main(sys.argv[0:])

