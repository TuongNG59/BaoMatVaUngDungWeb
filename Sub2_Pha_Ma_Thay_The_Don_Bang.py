ban_ma = input().strip()

tan_suat = {}

for ch in ban_ma:
    if ch in tan_suat:
        tan_suat[ch] += 1
    else:
        tan_suat[ch] = 1

danh_sach_sap_xep = sorted(tan_suat.items(), key=lambda x: x[1], reverse=True)

chu_E = danh_sach_sap_xep[0][0] 
chu_T = danh_sach_sap_xep[1][0] 
chu_A = danh_sach_sap_xep[2][0]  

print(f"{danh_sach_sap_xep[0][0]} {danh_sach_sap_xep[0][1]}")
print(f"{danh_sach_sap_xep[1][0]} {danh_sach_sap_xep[1][1]}")
print(f"{danh_sach_sap_xep[2][0]} {danh_sach_sap_xep[2][1]}")

ban_ro_nhap = ""
for ch in ban_ma:
    if ch == chu_E:
        ban_ro_nhap += 'E'
    elif ch == chu_T:
        ban_ro_nhap += 'T'
    elif ch == chu_A:
        ban_ro_nhap += 'A'
    else:
        ban_ro_nhap += '-'

print(ban_ro_nhap)