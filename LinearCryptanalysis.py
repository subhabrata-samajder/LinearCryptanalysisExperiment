import aes

import RC4 as rc4

import SmallPresent as SP

import numpy as np

import os

def FindMasksSubKey(n):
    NoOfNibbles = 4

    # Randomly generating a non-zero plaintext (or the input mask) and a non-zero last round mask (or the output Mask)
    # Using randint
#    InputMask = 0
#    while(InputMask == 0):
#        InputMask = int(np.random.randint(0, (1 << (4*n)), size = 1)[0])

    # Using AES in CTR mode
    # Initializing the key and iv (ctr) to use AES in CTR mode
    key = os.urandom(16)
    iv = os.urandom(16)

    Zero = 0
    # Sampling using AES in CTR mode
    if ((4*n) % 8 == 0):
        InputMask = aes.AES(key).encrypt_ctr(Zero.to_bytes(int((4*n)/8), "big"), iv)
        InputMask = int.from_bytes(InputMask, "big")
    else:
        InputMask = aes.AES(key).encrypt_ctr(Zero.to_bytes(int((4*n)/8) + 1, "big"), iv)
        InputMask = int.from_bytes(InputMask, "big")
        InputMask = (InputMask >> ((4*n) - (8*int((4*n)/8))))

    # Incrementing the ctr by 1
    iv = int.from_bytes(iv, "big") + 1
    iv = iv.to_bytes(16, "big")

    OutputMask = 0
    if ((4*n) <= 16):
        # Using randint
        while(OutputMask == 0):
            OutputMask = int(np.random.randint(0, (1 << (4*n)), size = 1)[0])
    else:
        # Using randint
        OutputMask = 0
        while(OutputMask == 0):
            for i in range(NoOfNibbles):
                NibbleNo = int(np.random.randint(0, n, size = 1)[0])
            
                if ((OutputMask & (15 << (4*NibbleNo))) == 0):
                    OutputMask ^= (int(np.random.randint(0, 16, size = 1)[0]) << (4*NibbleNo))

#        # Using AES in CTR mode
#        # Sampling using AES in CTR mode
#        if ((4*n) % 8 == 0):
#            OutputMask = aes.AES(key).encrypt_ctr(Zero.to_bytes(int((4*n)/8), "big"), iv)
#            OutputMask = int.from_bytes(OutputMask, "big")
#        else:
#            OutputMask = aes.AES(key).encrypt_ctr(Zero.to_bytes(int((4*n)/8) + 1, "big"), iv)
#            OutputMask = int.from_bytes(OutputMask, "big")
#            OutputMask = (OutputMask >> ((4*n) - (8*int((4*n)/8))))

    # Calculating the number of (r + 1)-round and r-round subkey bits. Here m denotes the number of non-zero nibbles in the OutputMask. Therefore,
    # the total number of subkey bits is 2*(4*m).
    m = 0
    SubKeyNibblesR = []
    for i in range(n):
        if ((OutputMask & (15 << (4*i))) != 0):
            m += 1

            SubKeyNibblesR.append(i)

    return InputMask, OutputMask, m, SubKeyNibblesR

def KeyGuess(m, r, RoundKeys, SubKeyNibblesR):
    if ((4*m) >= 64):
        # Initializing the key and iv (ctr) to use AES in CTR mode
        key = os.urandom(16)
        iv = os.urandom(16)

        Zero = 0

    # Making an (r + 1)-round and r-round wrong key guess
    FlagR = 0
    FlagR1 = 0
    while((FlagR == 0) or (FlagR1 == 0)):
        # Making an (r + 1)-round wrong key guess
        if (FlagR1 == 0):
            if ((4*m) < 64):
                # Using randint
                KeyGuessR1 = int(np.random.randint(0, (1 << 4*m), size = 1)[0])
            else:
                # Sampling using AES in CTR mode
                if ((4*m) % 8 == 0):
                    KeyGuessR1 = aes.AES(key).encrypt_ctr(Zero.to_bytes(int((4*m)/8), "big"), iv)
                    KeyGuessR1 = int.from_bytes(KeyGuessR1, "big")
                else:
                    KeyGuessR1 = aes.AES(key).encrypt_ctr(Zero.to_bytes(int((4*m)/8) + 1, "big"), iv)
                    KeyGuessR1 = int.from_bytes(KeyGuessR1, "big")
                    KeyGuessR1 = (KeyGuessR1 >> ((4*m) - (8*int((4*m)/8))))

                # Incrementing the ctr by 1
                iv = int.from_bytes(iv, "big") + 1
                iv = iv.to_bytes(16, "big")

        # Making an r-round wrong key guess
        if (FlagR == 0):
            if ((4*m) < 64):
                # Using randint
                KeyGuessR = int(np.random.randint(0, (1 << 4*m), size = 1)[0])
            else:
                # Sampling using AES in CTR mode
                if ((4*m) % 8 == 0):
                    KeyGuessR = aes.AES(key).encrypt_ctr(Zero.to_bytes(int((4*m)/8), "big"), iv)
                    KeyGuessR = int.from_bytes(KeyGuessR, "big")
                else:
                    KeyGuessR = aes.AES(key).encrypt_ctr(Zero.to_bytes(int((4*m)/8) + 1, "big"), iv)
                    KeyGuessR = int.from_bytes(KeyGuessR, "big")
                    KeyGuessR = (KeyGuessR >> ((4*m) - (8*int((4*m)/8))))
    
        TempKeyR = 0
        TempKeyR1 = 0
        Mask = 0
        for i in range(len(SubKeyNibblesR)):
            TempKeyR1 ^= (((KeyGuessR1 & (15 << (4*i))) >> (4*i)) << (4*SubKeyNibblesR[i]))
            TempKeyR ^= (((KeyGuessR & (15 << (4*i))) >> (4*i)) << (4*SubKeyNibblesR[i]))

            Mask ^= (15 << (4*SubKeyNibblesR[i]))

        if ((Mask & RoundKeys[r]) != TempKeyR1):
            KeyGuessR1 = TempKeyR1
            FlagR1 = 1

        if ((Mask & RoundKeys[r - 1]) != TempKeyR):
            KeyGuessR = TempKeyR
            FlagR = 1

    return KeyGuessR, KeyGuessR1

def LinearCryptanalysis(PlaintextSampleChoice, n, r, KeyLen, RoundKeys, InputMask, OutputMask, m, SubKeyNibblesR, N, KeyGuessR, KeyGuessR1):
    # Calculating the inverse S-box
    Sbox = [12, 5, 6, 11, 9, 0, 10, 13, 3, 14, 15, 8, 4, 7, 1, 2]
    SboxInv = [Sbox.index(x) for x in range(16)]

    if(4*n % 8 != 0): 
        Rem = 1 
    else:
        Rem = 0

    if (PlaintextSampleChoice == 1):                                                                                     # Use AES in CTR Mode
        # Initilizing the key and iv (ctr) of AES in CTR mode
        key = os.urandom(16)
        iv = os.urandom(16)
    elif (PlaintextSampleChoice == 2):                                                                                   # Use RC4
        RC4KeyLen = 40
        RC4Key = rc4.SelectKey(RC4KeyLen)

        State = rc4.KSA(RC4Key, RC4KeyLen)

        Iter1 = 0
        Iter2 = 0


    # Calculaing the number of times the linear approximation is equal to 1 out of N plaintext-ciphertext pairs
    Count = 0
    Zero = 0
    for i in range(N):
        # Randomly generating a plaintext
        if (PlaintextSampleChoice == 1):
            # Sampling using AES in CTR mode
            Plaintext = aes.AES(key).encrypt_ctr(Zero.to_bytes(int((4*n)/8) + Rem, "big"), iv)
            Plaintext = int.from_bytes(Plaintext, "big")
            Plaintext = (Plaintext >> ((8*(int((4*n)/8) + Rem)) - (4*n)))

            # Incrementing the ctr by 1
            iv = int.from_bytes(iv, "big") + 1
            iv = iv.to_bytes(16, "big")
        elif (PlaintextSampleChoice == 2):
            for j in range(int((4*n)/8) + Rem):
                Plaintext1, State, Iter1, Iter2 = rc4.PRGA_OneByte(State, Iter1, Iter2)

                if (j == (int((4*n)/8) + Rem - 1)):
                    Plaintext1 = (Plaintext1 >> ((8*(int((4*n)/8) + Rem)) - 4*n))

                    Plaintext = int("%s%s" %(hex(Plaintext), hex(Plaintext1)[2:]), 16)
                elif (j != 0):
                    Plaintext = int("%s%s" %(hex(Plaintext), hex(Plaintext1)[2:]), 16)
                elif (j == 0):
                    Plaintext = Plaintext1

        # Evaluation of Plaintext Mask
        XOR = 0
        Temp = (InputMask & Plaintext)
        for j in range(4*n):
            XOR ^= ((Temp & (1 << j)) >> j)

        # Calculating the corresponding ciphertext output of Small-Present under the key "RoundKeys"
        Ciphertext = SP.SmallPresent(n, r, Plaintext, RoundKeys, KeyLen)

        # Evaluation of Ciphertext Mask
        # Inverse Permuation
        PartialState = 0
        for j in range(4*n):
           if (j != (4*n - 1)):
               Bit = ((Ciphertext & (1 << j)) >> j)
               PartialState ^= (Bit << ((4*j)%(4*n - 1)))
           else:
               Bit = ((Ciphertext & (1 << j)) >> j)
               PartialState ^= (Bit << (4*n - 1))

        # Inverse Key XOR
        PartialState ^= KeyGuessR1

        # Inverse SBox
        PartialStateNew = 0
        for j in range(n):
            Nibble = ((PartialState & (15 << (4*j))) >> (4*j))
            
            PartialStateNew ^= (SboxInv[Nibble] << (4*j))

        PartialState = PartialStateNew

       # Inverse Key XOR
        PartialState ^= KeyGuessR

        # Evaluting Outputmask
        PartialState = (OutputMask & PartialState)

        for j in range(4*n):
            XOR ^= ((PartialState & (1 << j)) >> j)

        Count += XOR

    return Count
