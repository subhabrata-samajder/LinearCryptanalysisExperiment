import os, sys

def Swap(a, b):
    t = a
    a = b
    b = t

    return a, b

def SelectKey(KeyLen):
    Key = []
    
    for i in range(KeyLen):
        Key.append(int.from_bytes(os.urandom(1), "big"))

    return Key

def KSA(Key, KeyLen):
    S = [i for i in range(1 << 8)]

    j = 0
    for i in range(1 << 8):
        j = (j + S[i] + Key[i % KeyLen]) % 256

        S[i], S[j] = Swap(S[i], S[j])

    return S

def PRGA_OneByte(S, i, j):
    i = (i + 1) % 256
#    print(i)
    j = (j + S[i]) % 256

    S[i], S[j] = Swap(S[i], S[j])

    return S[(S[i] + S[j]) % 256], S, i, j

def PRGA(S, NoOfBytes):
    Output = []
    i = 0
    j = 0

    for l in range(NoOfBytes):
        Out, S, i, j = PRGA_OneByte(S, i, j)
        Output.append(Out)

    return S, Output

def TestRC4():
    #----Test Vectors 1----#
    KeyLen = 3
    Key = [ord('K'), ord('e'), ord('y')]
    OutputLen = 10
    OutputStream = [int("0xEB", 16), int("0x9F", 16), int("0x77", 16), int("0x81", 16), int("0xB7", 16), int("0x34", 16), int("0xCA", 16), int("0x72", 16), int("0xA7", 16), int("0x19", 16)]

    S = KSA(Key, KeyLen)

    S, Output = PRGA(S, OutputLen)

    for i in range(OutputLen):
        print("%s" %hex(Output[i])[2:], end="")
    print("")

    for i in range(OutputLen):
        if (OutputStream[i] != Output[i]):
            print("%s: %s != %s" %(i, OutputStream[i], Output[i]))

            return 1

    if (i == OutputLen - 1):
        print("Test 1 passed successfully!")

    #----Test Vectors 2----#
    KeyLen = 4
    Key = [ord('W'), ord('i'), ord('k'), ord('i')]
    OutputLen = 6
    OutputStream = [int("0x60", 16), int("0x44", 16), int("0xDB", 16), int("0x6D", 16), int("0x41", 16), int("0xB7", 16)]

    S = KSA(Key, KeyLen)

    S, Output = PRGA(S, OutputLen)

    for i in range(OutputLen):
        print("%s" %hex(Output[i])[2:], end="")
    print("")

    for i in range(OutputLen):
        if (OutputStream[i] != Output[i]):
            print("%s: %s != %s" %(i, OutputStream[i], Output[i]))

            return 1

    if (i == OutputLen - 1):
        print("Test 2 passed successfully!")

    #----Test Vectors 3----#
    KeyLen = 6
    Key = [ord('S'), ord('e'), ord('c'), ord('r'), ord('e'), ord('t')]
    OutputLen = 8
    OutputStream = [int("0x04", 16), int("0xD4", 16), int("0x6B", 16), int("0x05", 16), int("0x3C", 16), int("0xA8", 16), int("0x7B", 16), int("0x59", 16)]

    S = KSA(Key, KeyLen)

    S, Output = PRGA(S, OutputLen)

    for i in range(OutputLen):
        print("%s" %hex(Output[i])[2:], end="")
    print("")

    for i in range(OutputLen):
        if (OutputStream[i] != Output[i]):
            print("%s: %s != %s" %(i, OutputStream[i], Output[i]))

            return 1

    if (i == OutputLen - 1):
        print("Test 3 passed successfully!")

    return 0

def main(argv):
    n = 3

    if (TestRC4() == 1):
        print("Bug found!")

        return 1
    else:
        print("Tests passed successfully!")

    KeyLen = 40
    Key = SelectKey(KeyLen)

    State = KSA(Key, KeyLen)

    if(4*n % 8 != 0):
        Rem = 1
    else:
        Rem = 0

    print("Rem = %s" %Rem)

    Iter1 = 0
    Iter2 = 0
    for i in range(20):
            for j in range(int((4*n)/8) + Rem):
                Plaintext1, State, Iter1, Iter2 = PRGA_OneByte(State, Iter1, Iter2)

                print("%s" %hex(Plaintext1), end="\t")

                if (j == (int((4*n)/8) + Rem - 1)):
                    Plaintext1 = (Plaintext1 >> ((8*(int((4*n)/8) + Rem)) - 4*n))

                    Plaintext = int("%s%s" %(hex(Plaintext), hex(Plaintext1)[2:]), 16)
                elif (j != 0):
                    Plaintext = int("%s%s" %(hex(Plaintext), hex(Plaintext1)[2:]), 16)
                else:
                    Plaintext = int("0x%s" %(hex(Plaintext1)[2:]), 16)


            print("%s" %hex(Plaintext))

if __name__ == "__main__":
    main(sys.argv[0:])
