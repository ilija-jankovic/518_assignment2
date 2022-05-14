# MacOS: source venv/bin/activate
# https://nitratine.net/blog/post/python-encryption-and-decryption-with-pycryptodome/

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from matplotlib.pyplot import imread
import binascii
from PIL import Image
from io import BytesIO

image= imread('Image-Assignment2.bmp')

key = binascii.unhexlify('770A8A65DA156D24EE2A093277530142')

#AES.MODE_ECB
#AES.MODE_CBC
#AES.MODE_CFB

cipher = AES.new(key, AES.MODE_CFB)
p_bytes = image.tobytes()
left_over = len(p_bytes)%16
c_bytes = bytearray()

def get_c_bytes(block):
    return bytearray(cipher.encrypt(block)) 

def sub_bytes(p_bytes, len):
    return p_bytes[0:len]

for i in range(0, len(p_bytes), 16):
    block = p_bytes[i:i+16]
    c_bytes += get_c_bytes(block)

if(left_over > 0):
    block = pad(p_bytes[len(p_bytes)-left_over:len(p_bytes)], AES.block_size)
    c_bytes += get_c_bytes(block)

c_bytes = sub_bytes(c_bytes, len(p_bytes))

print(len(p_bytes), len(c_bytes))
image = Image.frombytes('RGB', (image.shape[1], image.shape[0]), bytes(c_bytes))
image.save('cfb.jpg')