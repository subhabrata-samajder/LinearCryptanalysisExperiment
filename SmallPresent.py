# Generates the round keys for the Small Present cipher 
def GenerateRoundKeys(Key, KeyLen, n, r, Sbox):
    RoundKeys = []

    for i in range(r + 1):
        RoundKey = ((1 << 64) - 1) << (KeyLen - 64)
        RoundKey = (RoundKey & Key) >> (KeyLen - 64)

        if (n == 16):
            RoundKeys.append(RoundKey)
        else:
            RoundKeys.append(RoundKey & ((1 << (4*n)) - 1))

        # Key Updation
        # 1. Left rotation by 61 bits
        Temp = Key
        Temp = (Temp << 61) & ((1 << KeyLen) - 1)
        Key = Temp ^ (Key >> (KeyLen - 61))

        # 2. Sbox Operation
        Temp = (15 << (KeyLen - 4)) 
        Temp = (Temp & Key) >> (KeyLen - 4)
        Temp = Sbox[int(Temp)]
        Key = ((Key << 4) & ((1 << KeyLen) - 1)) >> 4
        Key = Key ^ (Temp << (KeyLen - 4))

        # 3. XOR with round_counter (i + 1)
        Temp = ((i + 1) << 15)
        Key = Key ^ Temp

    return RoundKeys

# Bitwise XORing of the RoundKey with current internal State
def AddRoundKey(State, RoundKey):
    return (State ^ RoundKey)

# S-box layer of the Small Present round function
def SboxLayer(State, Sbox, n):
    NewState = 0

    for i in range(n):
        Val = 15
        Val = (Val << 4*i) & State
        Val = Sbox[Val >> 4*i]
        NewState ^= (Val << 4*i)

    return NewState

# Returns the permute State bits
def PermutationLayer(State, n):
    NewState = 0

    for i in range(4*n):
        if (i == 4*n - 1):
            NewState ^= ((1 << (4*n - 1)) & State)

        else:
            Bit = (((1 << i) & State) >> i)
           
            NewState ^= (Bit << ((n*i)%(4*n - 1)))

    return NewState

# Round function of Small Present
def RoundFunction(State, RoundKey, Sbox, n):
    State = AddRoundKey(State, RoundKey)
    State = SboxLayer(State, Sbox, n)
    State = PermutationLayer(State, n)

    return State


# Encryption algorithm of the Small Present cipher with block size n and number of rounds r
def SmallPresent(n, r, Plaintext, RoundKeys, KeyLen):
    Sbox = [12, 5, 6, 11, 9, 0, 10, 13, 3, 14, 15, 8, 4, 7, 1, 2]

    State = Plaintext
    for i in range(1, r + 1):
        State = RoundFunction(State, RoundKeys[i - 1], Sbox, n)
    
    State = AddRoundKey(State, RoundKeys[i])

    return State
