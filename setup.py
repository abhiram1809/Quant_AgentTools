from setuptools import setup, find_packages

setup(
    name='my-library',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'pydantic',
        'GPT4All'
    ],
)