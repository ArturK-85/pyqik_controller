from setuptools import setup

setup(
   name='pyqik_controller',
   version='0.1.0',
   author='Artur Komenda',
   author_email='artur.eu@protonmail.com',
   packages=['pyqik_controller'],
   scripts=['bin/pololu_crc7.so'],
   url='http://pypi.python.org/pypi/pyqik_controller/',
   license='LICENSE',
   description='A Python Pololu QIK Controller Library',
   long_description=open('README.md').read()
)
