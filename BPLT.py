def power_mod(a, x, n):
    ans = 1
    base = a % n
    exp = x
    
    while exp > 0:
        if exp % 2 == 1:
            ans = (ans * base) % n

        base = (base * base) % n

        exp //= 2
        
    return ans

a, x, n = map(int, input().split())

result = power_mod(a, x, n)
print(result)