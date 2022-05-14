# MacOS: source venv/bin/activate
# https://nitratine.net/blog/post/python-encryption-and-decryption-with-pycryptodome/

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from matplotlib.pyplot import imread
import binascii

image= imread('Image-Assignment2.bmp')

key = binascii.unhexlify('770A8A65DA156D24EE2A093277530142')

#AES.MODE_ECB
#AES.MODE_CBC
#AES.MODE_CFB

cipher = AES.new(key, AES.MODE_EAX)
bytes = image.tobytes()
left_over = len(bytes)%16
c_bytes = []

def get_c_bytes(block):
    c_block = cipher.encrypt(block)
    c_bytes = []
    for i in range(0, 16):
        c_bytes.append(c_block[i:i+1])
    return c_bytes

def sub_bytes(bytes, len):
    return bytes[0:len]

for i in range(0, len(bytes), 16):
    block = bytes[i*16:(i+1)*16]
    c_bytes += get_c_bytes(block)

if(left_over > 0):
    block = pad(bytes[len(bytes)-left_over:len(bytes)], AES.block_size)
    c_bytes += get_c_bytes(block)

c_bytes = sub_bytes(c_bytes, len(bytes))

print(len(bytes), len(c_bytes))