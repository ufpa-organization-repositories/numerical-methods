import os
import sys
import importlib
from typing import List, Optional
import base64
import io


class Utils:    
    @staticmethod
    def serialize_image(path_image: str) -> str:
        """[SERVER] Serialize a photo (read bytes -> encode 64 -> str (utf-8))
        to send it through the network
        :path_photo: str
        return: str
        """    

        abs_path_to_image_name: str = path_image
        image: _io.BufferedReader = open(abs_path_to_image_name, 'rb')
        image_read: bytes = image.read()
        image_64_encode: bytes = base64.encodebytes(image_read)
        image_str: str = image_64_encode.decode(encoding="utf-8")
        return image_str
    
    @staticmethod
    def load_module(module_name: str, path: str):
        # https://www.dev2qa.com/how-to-import-a-python-module-from-a-python-file-full-path/

        spec = importlib.util.spec_from_file_location(module_name.replace(".py", ""), os.path.join(path, module_name))        
        module_object = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module_object)
        print('module: ', module_name, module_object)
        print('module type: ', type(module_object))
        return module_object
    
    @staticmethod
    def set_module_objects_to_built_in(module_object) -> None:
        for key in module_object.__dict__:
            if not "__" in key:
                print(key, module_object.__dict__[key])
                setattr(__builtins__, key, module_object.__dict__[key])
    
    @staticmethod
    def get_images_from_directory(path) -> List:

        server_path: str = os.getcwd()
        
        os.chdir(path)

        image_extensions = ["png", "jpg", "jpeg"]
        li_images: List[str] = []
        for file in os.listdir(path):                        
            extension = file.split(".")[-1]
            print(f'file: {file}')
            if extension in image_extensions:
                print(f'{file} is image file')
                # issue: return the bytes of the image
                # create a method to do that
                li_images.append(file)
        
        os.chdir(server_path)
        return li_images

    @staticmethod
    def import_module(path: str) -> None:
        sys.path.append(path)