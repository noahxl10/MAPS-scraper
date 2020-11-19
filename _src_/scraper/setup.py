from setuptools import setup 
from Cython.Build import cythonize  
setup(
    ext_modules = cythonize("*.pyx", annotate=True)
)  
#  python setup.py build_ext --inplace
