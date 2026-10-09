from Crypto.Cipher import DES

def pad(tmp):
    n = len(tmp) % 8
    if n > 0: 
        n = 8 - n
    return tmp + (b' ' * n)

key = input().encode()
plain = input().encode()

padded = pad(plain)

des = DES.new(key, DES.MODE_ECB)
cipher = des.encrypt(padded)

print(len(cipher))

for v in cipher: 
    print(v, end=' ')
print()

tmp = des.decrypt(cipher)  
text = tmp.decode().rstrip(' ')
print(text)