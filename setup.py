from setuptools import setup, find_packages

setup(
    name='Quant_AgentTools',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'pydantic',
        'GPT4All'
    ],
)