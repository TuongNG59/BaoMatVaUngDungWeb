import urllib.request
import hashlib

url = input().strip()

# Download nội dung file từ URL
with urllib.request.urlopen(url, timeout=10) as response:
    content = response.read()

# Tính giá trị băm
md5_hash = hashlib.md5(content).hexdigest()
sha256_hash = hashlib.sha256(content).hexdigest()

# In kết quả
print(md5_hash)
print(sha256_hash)