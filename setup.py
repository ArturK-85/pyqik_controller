from setuptools import setup, Extension

module = Extension('pololu_crc7', sources = ['src/pololu_crc7.c'])

setup(
   name='pyqik_controller',
   version='0.1.0',
   author='Artur Komenda',
   author_email='artur.eu@protonmail.com',
   packages=['pyqik_controller'],
   ext_modules = [module],
   url='http://pypi.python.org/pypi/pyqik_controller/',
   license='LICENSE',
   description='A Python Pololu QIK Controller Library',
   long_description=open('README.md').read()
)
