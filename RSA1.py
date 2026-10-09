def mod_inverse(e, phi_n):
    mod = phi_n
    x0, x1 = 0, 1
    a = e
    n = phi_n
    while a > 1:
        q = a // n
        a, n = n, a % n
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += mod
    return x1

def power_mod(base, exp, mod):
    ans = 1
    base = base % mod
    while exp > 0:
        if exp % 2 == 1:
            ans = (ans * base) % mod
        base = (base * base) % mod
        exp //= 2
    return ans

def solve():
    p, q, e, M = map(int, input().split())

    N = p * q
    phi_N = (p - 1) * (q - 1)

    d = mod_inverse(e, phi_N)

    C = power_mod(M, d, N)

    decrypted_M = power_mod(C, e, N)

    print(f"{e} {N}") 
    print(f"{d} {N}")  
    print(C)          
    print(decrypted_M) 

if __name__ == "__main__":
    solve()