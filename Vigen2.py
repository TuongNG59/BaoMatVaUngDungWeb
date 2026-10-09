ban_ma = input().strip()
ban_ro = input().strip()

chuoi_khoa_day_du = ""
for i in range(len(ban_ma)):
    c = ord(ban_ma[i]) - ord('A')
    p = ord(ban_ro[i]) - ord('A')
    
    k_i = (c - p) % 26
    
    chuoi_khoa_day_du += chr(k_i + ord('A'))

n = len(chuoi_khoa_day_du)

for L in range(2, n + 1):
    la_khoa_chu_ky = True
    
    for i in range(n):
        if chuoi_khoa_day_du[i] != chuoi_khoa_day_du[i % L]:
            la_khoa_chu_ky = False
            break
            
    if la_khoa_chu_ky:
        khoa_k = chuoi_khoa_day_du[:L]
        print(khoa_k)
        break