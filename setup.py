from setuptools import setup, find_packages

version = '0.0.2'

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

    # requests-cache should be added here when the version in pypi supports
    # ignored_parameters. Unitl then cache will not work without manually
    # installing the version from github.
    #
    # TODO: Cache this missing module in the code and print instructions
    #       for installing it.
    install_requires=['marshmallow', 'requests'],
    )
