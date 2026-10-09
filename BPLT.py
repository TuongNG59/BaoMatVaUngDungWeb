def power_mod(a, x, n):
    ans = 1
    base = a % n
    exp = x
    
    while exp > 0:
        # Nếu bit cuối của exp là 1 (số lẻ)
        if exp % 2 == 1:
            ans = (ans * base) % n
        
        # Bình phương base cho bước tiếp theo
        base = (base * base) % n
        
        # Giảm exp đi một nửa
        exp //= 2
        
    return ans

# 1. Nhập 3 số a, x, n trên cùng một dòng
a, x, n = map(int, input().split())

# 2. Tính và in kết quả
result = power_mod(a, x, n)
print(result)