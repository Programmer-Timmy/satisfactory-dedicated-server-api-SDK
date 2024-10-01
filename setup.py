from setuptools import setup, find_packages

setup(
    name='satisfactory_api_client',
    version='0.1.2',
    packages=find_packages(),
    install_requires=[req.strip() for req in open('/requirements.txt').readlines()],
    description='A Python Package for interacting with the Satisfactory Dedicated Server API',
    long_description=open('README.md').read(),
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
