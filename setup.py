from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as file:
    long_description = file.read()

setup(
    name='Quant_AgentTools',
    version='0.2.5',
    description='Agentic Workflow with Quantized LLMs',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'pydantic',
        'GPT4All'
    ],
)