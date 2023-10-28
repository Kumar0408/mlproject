from setuptools import find_packages, setup
from typing import List

HYPEN_E_DOT = "-e ."
def get_requirements(file_path:str) -> List[str]:
    """
    function will return the list of packages
    """
    requirements=[]
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace("\n","")for req in requirements]   # replace the end line in req.txt with blank space

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
        
        print(requirements)
    
    return requirements

setup(
    name = 'mlproject',
    version = '0.0.1',
    author = 'Akshay',
    author_email= 'akshayrao0408@gmail.com',
    packages=  find_packages(),
    install_requires = get_requirements('requirements.txt')
)