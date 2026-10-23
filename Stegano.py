import sys
import urllib.request
from io import BytesIO
from PIL import Image

url = sys.stdin.readline().strip()
message = sys.stdin.readline().rstrip('\n\r')

with urllib.request.urlopen(url) as response:
    image = Image.open(BytesIO(response.read())).convert("RGB")

pixels = list(image.getdata())

bits = ''.join(format(ord(c), '08b') for c in message)
p = (len(bits) + 2) // 3

print(p)

bit_index = 0

for i in range(p):
    r, g, b = pixels[i]
    colors = [r, g, b]

    for j in range(3):
        if bit_index < len(bits):
            colors[j] = (colors[j] & 254) | int(bits[bit_index])
            bit_index += 1

    print(*colors)