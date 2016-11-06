from setuptools import setup, find_packages

version = '1.0.0'

setup(
    author_email='robert@rkuykendall.com',
    author='Robert Kuykendall',
    classifiers=[
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python",
        (
            "Topic :: Internet :: WWW/HTTP :: Dynamic Content "
            ":: CGI Tools/Libraries"
        ),
        "Topic :: Utilities",
    ],
    description="Marvel API python wrapper.",
    install_requires=['marshmallow', 'requests'],
    keywords='marvel api comics python',
    long_description=open("README.rst", "r").read(),
    name='marvelous',
    packages=find_packages(),
    url='http://github.com/rkuykendall/marvelous',
    version=version,
    zip_safe=True,
)
