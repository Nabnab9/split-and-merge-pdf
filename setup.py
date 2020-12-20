from setuptools import setup

setup(
    name='split-and-merge-pdf',
    version='1.0',
    description='Permet la jointure de plusieurs pdf toyota entre eux',
    author='Alban Rousseau',
    author_email='alban.rousseau9@gmail.com',
    packages=['split-and-merge-pdf'],  # same as name
    install_requires=['setuptools', 'Flask', 'Werkzeug', 'PyPDF2'],  # external packages as dependencies
)
