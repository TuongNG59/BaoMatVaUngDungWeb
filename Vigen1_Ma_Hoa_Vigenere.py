ban_ro = input().strip()
k = input().strip()

ban_ma = ""
do_dai_k = len(k)

for i in range(len(ban_ro)):
    p = ord(ban_ro[i]) - ord('A')
    k_i = ord(k[i % do_dai_k]) - ord('A')
    
    c = (p + k_i) % 26
    
    ban_ma += chr(c + ord('A'))
    
print(ban_ma)