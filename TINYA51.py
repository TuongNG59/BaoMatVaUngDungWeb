def majority(b1, b2, b3):
    return 1 if (b1 + b2 + b3) >= 2 else 0

def tiny_a5_1():
    x_str = input().strip()
    y_str = input().strip()
    z_str = input().strip()
    plaint = input().strip()

    X = [int(b) for b in x_str]
    Y = [int(b) for b in y_str]
    Z = [int(b) for b in z_str]

    cx, cy, cz = 1, 3, 3

    taps_x = [2, 4, 5]
    taps_y = [6, 7]
    taps_z = [2, 7, 8]
    
    ciphertext = []

    for bit in plaint:
        x, y, z = X[cx], Y[cy], Z[cz]
        maj = majority(x, y, z)

        if x == maj:
            fx = 0
            for t in taps_x:
                fx ^= X[t]
            X = [fx] + X[:-1]

        if y == maj:
            fy = 0
            for t in taps_y:
                fy ^= Y[t]
            Y = [fy] + Y[:-1]

        if z == maj:
            fz = 0
            for t in taps_z:
                fz ^= Z[t]
            Z = [fz] + Z[:-1]

        s = X[-1] ^ Y[-1] ^ Z[-1]

        c = int(bit) ^ s
        ciphertext.append(str(c))

    print("".join(ciphertext))

if __name__ == "__main__":
    tiny_a5_1()