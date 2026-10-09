ban_ro = input()
k = input()

ban_ma = ""

for ky_tu in ban_ro:
    if ky_tu == ' ':
        ban_ma += ' '
    else:
        vi_tri = ord(ky_tu) - ord('a')
        ban_ma += k[vi_tri]
print(ban_ma)