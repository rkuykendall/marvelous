from setuptools import setup, find_packages

version = '0.0.1'


def get_requirements():
    with open('requirements.txt') as f:
        # git here should be remoted when the version of requests-cache
        # in pypi supports ignored_parameters. Unitl then cache will not work
        # without manually installing the version from github.
        #
        # TODO: Cache this missing module in the code and print instructions
        #       for installing it.
        return [
            line for line in f.read().splitlines()
            if 'nose' not in line and 'git' not in line]

setup(
    name='marvelous',
    version='0.0.1',
    description="Marvel API python wrapper.",
    long_description=open("README.rst", "r").read(),
    author='Robert Kuykendall',
    author_email='robert@rkuykendall.com',
    url='http://github.com/rkuykendall/marvelous',
    packages=find_packages(),
    install_requires=get_requirements(),
    zip_safe=True,
    )
