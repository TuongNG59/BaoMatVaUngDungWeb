import math

ban_ro = input().strip()
k = list(input().strip())

num_cols = len(k)
num_rows = math.ceil(len(ban_ro) / num_cols)
total_chars = num_rows * num_cols

padding_char_code = ord('A')
while len(ban_ro) < total_chars:
    ban_ro += chr(padding_char_code)
    padding_char_code += 1

grid = []
for r in range(num_rows):
    row = list(ban_ro[r * num_cols : (r + 1) * num_cols])
    grid.append(row)

for i in range(num_cols - 1):
    min_idx = i
    for j in range(i + 1, num_cols):
        if k[j] < k[min_idx]:
            min_idx = j
            
    if min_idx != i:
        k[i], k[min_idx] = k[min_idx], k[i]

        for r in range(num_rows):
            grid[r][i], grid[r][min_idx] = grid[r][min_idx], grid[r][i]

ban_ma = ""
for c in range(num_cols):
    for r in range(num_rows):
        ban_ma += grid[r][c]

print(ban_ma)