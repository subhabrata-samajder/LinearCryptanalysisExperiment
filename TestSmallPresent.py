import SmallPresent as SP

import numpy as np

def main():
    Sbox = [12, 5, 6, 11, 9, 0, 10, 13, 3, 14, 15, 8, 4, 7, 1, 2]

    print("Verification for n = 2 (Plaintext = 0 and Key = 0):")
    Key = 0
    KeyLen = 80
    Nibbles = 2
    Rounds = 10

    RoundKeys = SP.GenerateRoundKeys(Key, KeyLen, Nibbles, Rounds, Sbox)

    Plaintext = 0

    print("Round\tState\tKey\tState XOR Key\tS(State XOR Key)")
    State = Plaintext
    for i in range(1, Rounds + 1):
        print("%s\t%s\t%s" %(i - 1, hex(State), hex(RoundKeys[i - 1])), end="")

        State = SP.AddRoundKey(State, RoundKeys[i - 1])
        print("\t%s" %(hex(State)), end="")

        State = SP.SboxLayer(State, Sbox, Nibbles)
        print("\t\t%s" %(hex(State)))

        State = SP.PermutationLayer(State, Nibbles)

    print("%s\t%s\t%s" %(Rounds, hex(State), hex(RoundKeys[Rounds])), end="")
    State = SP.AddRoundKey(State, RoundKeys[Rounds])
    print("\t%s" %(hex(State)), end="\n\n")

    print("Verification for n = 4 (Plaintext = 0 and Key = 0):")
    Key = 0
    KeyLen = 80
    Nibbles = 4
    Rounds = 10

    RoundKeys = SP.GenerateRoundKeys(Key, KeyLen, Nibbles, Rounds, Sbox)

    Plaintext = 0

    print("Round\tState\tKey\tState XOR Key\tS(State XOR Key)")
    State = Plaintext
    for i in range(1, Rounds + 1):
        print("%s\t%s\t%s" %(i - 1, hex(State), hex(RoundKeys[i - 1])), end="")

        State = SP.AddRoundKey(State, RoundKeys[i - 1])
        print("\t%s" %(hex(State)), end="")

        State = SP.SboxLayer(State, Sbox, Nibbles)
        print("\t\t%s" %(hex(State)))

        State = SP.PermutationLayer(State, Nibbles)

    print("%s\t%s\t%s" %(Rounds, hex(State), hex(RoundKeys[Rounds])), end="")
    State = SP.AddRoundKey(State, RoundKeys[Rounds])
    print("\t%s" %(hex(State)), end="\n\n")

    print("Verification for n = 8 (Plaintext = 0 and Key = 0):")
    Key = 0
    KeyLen = 80
    Nibbles = 8
    Rounds = 10

    RoundKeys = SP.GenerateRoundKeys(Key, KeyLen, Nibbles, Rounds, Sbox)

    Plaintext = 0

    print("Round\tState\t\tKey\t\tState XOR Key\tS(State XOR Key)")
    State = Plaintext
    for i in range(1, Rounds + 1):
        if(i == 1):
            print("%s\t%s\t\t%s" %(i - 1, hex(State), hex(RoundKeys[i - 1])), end="")
        else:
            print("%s\t%s\t%s" %(i - 1, hex(State), hex(RoundKeys[i - 1])), end="")

        State = SP.AddRoundKey(State, RoundKeys[i - 1])
        if(i == 1):
            print("\t\t%s" %(hex(State)), end="")
        elif ((i == 2) or (i == 3)) :
            print("\t\t%s" %(hex(State)), end="")
        else:
            print("\t%s" %(hex(State)), end="")

        State = SP.SboxLayer(State, Sbox, Nibbles)
        if(i == 1):
            print("\t\t%s" %(hex(State)))
        else:
            print("\t%s" %(hex(State)))

        State = SP.PermutationLayer(State, Nibbles)

    print("%s\t%s\t%s" %(Rounds, hex(State), hex(RoundKeys[Rounds])), end="")
    State = SP.AddRoundKey(State, RoundKeys[Rounds])
    print("\t%s" %(hex(State)), end="\n\n")

    print("Verification for n = 16 (Plaintext = 0 and Key = 0):")
    Key = 0
    KeyLen = 80
    Nibbles = 16
    Rounds = 10

    RoundKeys = SP.GenerateRoundKeys(Key, KeyLen, Nibbles, Rounds, Sbox)

    Plaintext = 0

    print("Round\tState\t\t\tKey\t\t\tState XOR Key\t\tS(State XOR Key)")
    State = Plaintext
    for i in range(1, Rounds + 1):
        if (i == 1):
            print("%s\t%s\t\t\t%s" %(i - 1, hex(State), hex(RoundKeys[i - 1])), end="")
        else:
            print("%s\t%s\t%s" %(i - 1, hex(State), hex(RoundKeys[i - 1])), end="")

        State = SP.AddRoundKey(State, RoundKeys[i - 1])
        if (i == 1):
            print("\t\t\t%s" %(hex(State)), end="")
        elif (i == 7):
            print("\t\t%s" %(hex(State)), end="")
        else:
            print("\t%s" %(hex(State)), end="")

        State = SP.SboxLayer(State, Sbox, Nibbles)
        if (i == 1):
            print("\t\t\t%s" %(hex(State)))
        elif (i == 7):
            print("\t%s" %(hex(State)))
        else:
            print("\t%s" %(hex(State)))

        State = SP.PermutationLayer(State, Nibbles)

    print("%s\t%s\t%s" %(Rounds, hex(State), hex(RoundKeys[Rounds])), end="")
    State = SP.AddRoundKey(State, RoundKeys[Rounds])
    print("\t%s" %(hex(State)), end="\n")

if __name__ == "__main__":
    main()
