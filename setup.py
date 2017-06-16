from setuptools import setup, find_packages

readme = open('README.rst').read()
history = open('CHANGES.rst').read().replace('.. :changelog:', '')

setup(
    name="docker-registry-client",
    version='0.5.2',
    description='Client for Docker Registry V1 and V2',
    long_description=readme + '\n\n' + history,
    author='John Downs',
    author_email='john.downs@yodle.com',
    url='https://github.com/yodle/docker-registry-client',
    license="Apache License 2.0",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: System :: Software Distribution',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='docker docker-registry REST',
    packages=find_packages(),
    install_requires=[
        'requests>=2.4.3, <3.0.0',
        'ecdsa>=0.13.0, <0.14.0',
        'jws>=0.1.3, <0.2.0',
    ],
)
