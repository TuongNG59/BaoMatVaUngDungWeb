import hashlib

password = input().strip()

password_bytes = password.encode('utf-8')

md5_hash = hashlib.md5(password_bytes).hexdigest()

sha256_hash = hashlib.sha256(password_bytes).hexdigest()

print(md5_hash)
print(sha256_hash)