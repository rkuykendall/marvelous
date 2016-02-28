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
    install_requires=[
        'requests', 'marshmallow',
        'https://github.com/reclosedev/requests-cache/tarball/master'
        '#egg=request-cache-0.4.11beta'],  # Needed until next release > 0.4.10
    zip_safe=True,
    )
