# MacOS: source venv/bin/activate
# https://nitratine.net/blog/post/python-encryption-and-decryption-with-pycryptodome/

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from matplotlib.pyplot import imread
import binascii
from PIL import Image

key = binascii.unhexlify('770A8A65DA156D24EE2A093277530142')
image = imread('Image-Assignment2.bmp')

class AESImageEncryption:
    def __update_params(self, mode):
        self.__mode = mode;
        self.__cipher = AES.new(self.__key, mode)

    def __init__(self, key, image, mode):
        self.__key = key
        self.__p_bytes = image.tobytes()
        self.__update_params(mode)

    def change_mode(self, mode):
        self.__update_params(mode)

    def encrypt(self):
        if(self.__mode != AES.MODE_CFB):
            c_bytes = self.__cipher.encrypt(pad(self.__p_bytes, AES.block_size))
            left_over = len(self.__p_bytes) % 16
            c_bytes = c_bytes[0:len(c_bytes)-left_over]
        else:
            c_bytes = self.__cipher.encrypt(self.__p_bytes)
        return Image.frombytes('RGB', (image.shape[1], image.shape[0]), bytes(c_bytes))

image_enc = AESImageEncryption(key, image, AES.MODE_ECB)
c_image = image_enc.encrypt()
c_image.save('ecb.jpg')

image_enc.change_mode(AES.MODE_CBC)
c_image = image_enc.encrypt()
c_image.save('cbc.jpg')

image_enc.change_mode(AES.MODE_CFB)
c_image = image_enc.encrypt()
c_image.save('cfb.jpg')