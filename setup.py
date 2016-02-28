from setuptools import setup, find_packages

version = '0.0.1'


def get_requirements():
    with open('requirements.txt') as f:
        return [line for line in f.read().splitlines() if 'nose' not in line]

setup(
    name='marvelous',
    version='0.0.1',
    description="Marvel API python wrapper.",
    long_description=open("README.md", "r").read(),
    author='Robert Kuykendall',
    author_email='robert@rkuykendall.com',
    url='http://github.com/rkuykendall/marvelous',
    packages=find_packages(),
    install_requires=get_requirements(),
    zip_safe=True,
    )
