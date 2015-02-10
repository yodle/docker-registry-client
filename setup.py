from setuptools import setup, find_packages
setup(
    name="dockerregistryclient",
    version="0.1",
    packages=find_packages(),
    install_requires=['requests>=2.4.3',
                      'mock>=1.0.1'],
    license="Apache License 2.0"
)