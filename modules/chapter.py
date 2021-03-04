import os
from abc import ABC, abstractmethod
from typing import List, Dict
import re


class Chapter(ABC):
    """Chapter operations"""

    @staticmethod
    def get_chapters() -> List[str]:

        chapters_path: str = os.path.join(os.getcwd(), "methods")
        chapters: List[str] = os.listdir(chapters_path)
        return chapters

    
    @staticmethod
    def get_chapter_methods(chapter_name) -> List[str]:
        """Get the methods of the selected chapter"""

        chapters_path = os.path.join(os.getcwd(), "methods")
        chapters = os.listdir(chapters_path)

        for chapter in chapters:            
            l_ocorrences: list = re.findall(chapter_name, chapter)
            if len(l_ocorrences) > 0:
                chapter_methods: Dict = {"methods": os.listdir(os.path.join(chapters_path, chapter))}
                print('ocorrences: ', l_ocorrences)
                print('methods: ', chapter_methods)
                return chapter_methods
