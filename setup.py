import os

from setuptools import setup, find_packages
root_dir = os.path.abspath(os.path.dirname(__file__))

# Construct the path to requirements.txt in the root directory
readme_path = os.path.join(root_dir, 'README.md')

setup(
    name='satisfactory_api_client',
    version='0.1.12',
    packages=find_packages(exclude=['tests', 'examples']),
    install_requires=[
        "python-dotenv~=1.0.1",
        "requests~=2.32.3"
    ],
    description='A Python Package for interacting with the Satisfactory Dedicated Server API',
    long_description=open(readme_path).read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Programmer-Timmy/satisfactory-dedicated-server-api-SDK',  # Replace with your repo URL
    author='Programmer-Timmy',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
