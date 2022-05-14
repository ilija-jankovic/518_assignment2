# Checks imports incase venv was not activated.
try:
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import pad
    from matplotlib.pyplot import imread
    import binascii
    from PIL import Image
    import sys
except:
    print('Please go to the source directory and type\nsource venv/bin/activate\nto activate the virtual environment.')
    exit()
    
def verbose_exit():
    print('Usage: python part2.py [input path] [output path]')
    exit(0)

# Checks for correct number of non-empty arguments.
if(len(sys.argv) < 3 or len(sys.argv[1]) == '' or len(sys.argv[2]) == ''):
    print('Please enter the path of the BMP file to encrypt and a directory to save the encrypted JPG outputs.')
    verbose_exit()

bmp_path = sys.argv[1]

# Ensures only a BMP file can be selected as the input.
tokens = bmp_path.split('.')
if(tokens[len(tokens)-1].lower() != 'bmp'):
    print('The input path must point to a BMP file.')
    verbose_exit()

output_path = sys.argv[2]

# Remove slash to format directory for output.
if output_path[len(output_path)-1] == '/':
    output_path = output_path[0:len(output_path-1)]

# The image file attempts to be read as a numpy array.
try:
    image = imread(bmp_path)
except:
    print(f'Could not load BMP file {bmp_path}. Please try restarting the program with a valid path.')
    verbose_exit()

# Key is constant as per the assignment specifications.
key = binascii.unhexlify('770A8A65DA156D24EE2A093277530142')

# A class to manage AES image encryption logic. Useful to be explictly defined for different AES modes.
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

    # Creates and returns the encrypted the image based on the mode parameter.
    def encrypt(self):
        # If the mode is not CFB, the data must be padded with the AES block size of 128 bits.
        if(self.__mode != AES.MODE_CFB):
            c_bytes = self.__cipher.encrypt(pad(self.__p_bytes, AES.block_size))

            # The padded bytes are stripped away as these would interfere with image creation.
            left_over = len(self.__p_bytes) % 16
            c_bytes = c_bytes[0:len(c_bytes)-left_over]
        else:
            c_bytes = self.__cipher.encrypt(self.__p_bytes)
        
        # The image is created based on the rows and columns of the original image and the ciphertext bytes.
        return Image.frombytes('RGB', (image.shape[1], image.shape[0]), bytes(c_bytes))

# Attempts to encrypt and output three JPG files, based on modes ECB, CBC, and CFB.
# If an error occurs, the output path was most likely incorrect.
try:
    image_enc = AESImageEncryption(key, image, AES.MODE_ECB)
    c_image = image_enc.encrypt()
    c_image.save(f'{output_path}/ecb.jpg')

    image_enc.change_mode(AES.MODE_CBC)
    c_image = image_enc.encrypt()
    c_image.save(f'{output_path}/cbc.jpg')

    image_enc.change_mode(AES.MODE_CFB)
    c_image = image_enc.encrypt()
    c_image.save(f'{output_path}/cfb.jpg')
except:
    print(f'Could not save image files at {output_path}.')
    verbose_exit()