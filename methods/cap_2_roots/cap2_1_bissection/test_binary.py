import base64
import io
import os

def serialize_image(path_photo: str) -> str:
    """[SERVER] Serialize a photo (read bytes -> encode 64 -> str (utf-8))
    to send it through the network
    :path_photo: str
    return: str
    """    

    abs_path_to_photo_name: str = path_photo
    image: _io.BufferedReader = open(abs_path_to_photo_name, 'rb')
    image_read: bytes = image.read()
    image_64_encode: bytes = base64.encodebytes(image_read)
    image_str: str = image_64_encode.decode(encoding="utf-8")
    return image_str

# image_str: str = serialize_image('ROOTs.png')
# print('image_str: ', image_str)