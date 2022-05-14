# MacOS: source venv/bin/activate
# https://nitratine.net/blog/post/python-encryption-and-decryption-with-pycryptodome/

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from matplotlib.pyplot import imread
import binascii
from PIL import Image

image = imread('Image-Assignment2.bmp')
key = binascii.unhexlify('770A8A65DA156D24EE2A093277530142')

class AESImageEncryption:
    def __update_params(self, mode):
        self.__mode = mode;
        self.__cipher = AES.new(key, mode)
        self.__left_over = len(self.__p_bytes)%16
        self.__c_bytes = bytearray()

    def __init__(self, image, mode):
        self.__p_bytes = image.tobytes()
        self.__update_params(mode)

    def change_mode(self, mode):
        self.__update_params(mode)

    def __encrypt_block(self, block):
        return bytearray(self.__cipher.encrypt(block)) 

    def __trim_cipher(self):
        self.__c_bytes = self.__c_bytes[0:len(self.__c_bytes)-self.__left_over]

    def encrypt(self):
        if(self.__mode != AES.MODE_CFB):
            for i in range(0, len(self.__p_bytes), 16):
                block = self.__p_bytes[i:i+16]
                self.__c_bytes += self.__encrypt_block(block)

            if(self.__left_over > 0):
                block = pad(self.__p_bytes[len(self.__p_bytes)-self.__left_over:len(self.__p_bytes)], AES.block_size)
                self.__c_bytes += self.__encrypt_block(block)

            self.__trim_cipher()
        else:
            self.__c_bytes = self.__cipher.encrypt(self.__p_bytes)

        return Image.frombytes('RGB', (image.shape[1], image.shape[0]), bytes(self.__c_bytes))

image_enc = AESImageEncryption(image, AES.MODE_ECB)
c_image = image_enc.encrypt()
c_image.save('ecb.jpg')

image_enc.change_mode(AES.MODE_CBC)
c_image = image_enc.encrypt()
c_image.save('cbc.jpg')

image_enc.change_mode(AES.MODE_CFB)
c_image = image_enc.encrypt()
c_image.save('cfb.jpg')