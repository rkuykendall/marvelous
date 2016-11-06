from setuptools import setup, find_packages

version = '0.0.4'

setup(
    name='marvelous',
    version=version,
    description="Marvel API python wrapper.",
    long_description=open("README.rst", "r").read(),
    author='Robert Kuykendall',
    author_email='robert@rkuykendall.com',
    url='http://github.com/rkuykendall/marvelous',
    packages=find_packages(),
    zip_safe=True,
    install_requires=['marshmallow', 'requests'],
    )
