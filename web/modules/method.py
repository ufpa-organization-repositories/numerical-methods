import os
from typing import List, Dict

class Method:
    """
    Execute the method
    """


    @staticmethod
    def execute(chapter_folder: str, method_folder: str):
        
        home_path: str = os.getcwd()        
        method_path: str = os.path.join(os.sep.join(os.getcwd().split(os.sep)[:-1]), "methods", chapter_folder, method_folder)
        print(method_path)
        os.chdir(method_path)
        os.system("python main.py")                        
        os.chdir(home_path)                