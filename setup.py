from setuptools import setup, find_packages

version = '0.0.1'

setup(
    name='marvelous',
    version='0.0.1',
    description="Marvel API python wrapper.",
    long_description=open("README.md", "r").read(),
    author='Robert Kuykendall',
    author_email='robert@rkuykendall.com',
    url='http://github.com/rkuykendall/marvelous',
    packages=find_packages(),
    install_requires=['requests'],
    zip_safe=True,
    )
