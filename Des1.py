from Cryptodome.Cipher import DES
from Cryptodome.Random import get_random_bytes
from Cryptodome.Util.Padding import pad

key_str = input().strip()
key = key_str.encode('utf-8')

n = int(input().strip())

plain_list = list(map(int, input().split()))
data = bytes(plain_list)

iv = get_random_bytes(8)

padded = pad(data, DES.block_size, 'pkcs7')

des = DES.new(key, DES.MODE_CBC, iv)

cipher_bytes = des.encrypt(padded)

result_bytes = iv + cipher_bytes

print(len(result_bytes))

result_str = [str(b) for b in result_bytes]
print(" ".join(result_str))