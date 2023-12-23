IP = [2, 6, 3, 1, 4, 8, 5, 7]
EP = [4, 1, 2, 3, 2, 3, 4, 1]
P4 = [2, 4, 3, 1]

S0 = [
    [1, 0, 3, 2],
    [3, 2, 1, 0],
    [0, 2, 1, 3],
    [3, 1, 3, 2]
]

S1 = [
    [0, 1, 2, 3],
    [2, 0, 1, 3],
    [3, 0, 1, 0],
    [2, 1, 0, 3]
]

IP_inverse = [4, 1, 3, 5, 7, 2, 8, 6]
P10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
P8 = [6, 3, 7, 4, 8, 5, 10, 9]


def apply_P10(bits):
    return [bits[P10[i] - 1] for i in range(len(P10))]

def apply_P8(bits):
    return [bits[P8[i] - 1] for i in range(len(P8))]

def apply_P4(bits):
    return [bits[P4[i] - 1] for i in range(len(P4))]

def apply_IP(bits):
    return [bits[IP[i] - 1] for i in range(len(IP))]

def apply_IP_inverse(bits):
    return [bits[IP_inverse[i] - 1] for i in range(len(IP_inverse))]

def apply_EP(bits):
    return [bits[EP[i] - 1] for i in range(len(EP))]


def lshift(bits, shift):
    return [bits[(i + shift) % len(bits)] for i in range(len(bits))]

def SubKeyGen(key):
    key = list(f"{key:010b}")
    key = apply_P10(key)
    rkey = key[:5]
    lkey = key[5:]
    key = lshift(rkey, 1) + lshift(lkey, 1)
    k1 = apply_P8(key)
    key = lshift(rkey, 3) + lshift(lkey, 3)
    k2 = apply_P8(key)
    return k1, k2

def subBox0(bits):
    row = int(str(bits[0] + bits[3]), 2)
    col = int(str(bits[1] + bits[2]), 2)
    bits = f"{S0[row][col]:02b}"
    return [bits[0], bits[1]]

def subBox1(bits):
    row = int(str(bits[0] + bits[3]), 2)
    col = int(str(bits[1] + bits[2]), 2)
    bits = f"{S0[row][col]:02b}"
    return [bits[0], bits[1]]

def xor(b1, b2):
    return [str(int(i) ^ int(j)) for i, j in zip(b1, b2)]

def Fk(bits, k):
    bits = apply_EP(bits)
    bits = xor(bits, k)
    bits = subBox0(bits[:4]) + subBox1(bits[4:])
    return apply_P4(bits)


def fk(lbits, rbits, k):
    return xor(lbits, Fk(rbits, k)), rbits

def enc(bits, k1, k2):
    bits = apply_IP(bits)
    lbits, rbits = bits[:4], bits[4:]
    lbits, rbits = fk(lbits, rbits, k1)
    lbits, rbits = rbits, lbits
    lbits, rbits = fk(lbits, rbits, k2)
    bits = apply_IP_inverse(lbits + rbits)
    return bits

def dec(bits, k1, k2):
    bits = apply_IP(bits)
    lbits, rbits = bits[:4], bits[4:]
    lbits, rbits = fk(lbits, rbits, k2)
    lbits, rbits = rbits, lbits
    lbits, rbits = fk(lbits, rbits, k1)
    bits = apply_IP_inverse(lbits + rbits)
    return bits


def s_des_enc(message, key):
    k1, k2 = SubKeyGen(key)
    ct = []
    for i in message:
        bits = f"{i:08b}"
        bits = enc(bits, k1, k2)  
        ct += [int("".join(bits), 2)]
    return bytes(ct)

def s_des_dec(ct, key):
    k1, k2 = SubKeyGen(key)
    message = []
    for i in ct:
        bits = f"{i:08b}"
        bits = dec(bits, k1, k2)  
        message += [int("".join(bits), 2)]
    return bytes(message)



# if __name__ == "__main__":
#     message = "Hello World".encode("utf-8")
#     key = 1000
#     print(message.decode())
#     ct = s_des_enc(message, key)
#     print(ct)
#     m = s_des_dec(ct, key)
#     print(m.decode())