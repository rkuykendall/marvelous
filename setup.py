from setuptools import find_packages, setup

version = "1.4.1"

setup(
    author_email="robert@rkuykendall.com",
    author="Robert Kuykendall and Contributors",
    classifiers=[
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python",
        ("Topic :: Internet :: WWW/HTTP :: Dynamic Content " ":: CGI Tools/Libraries"),
        "Topic :: Utilities",
    ],
    description="Marvel API wrapper for python.",
    install_requires=["marshmallow", "requests"],
    keywords="marvel api comics python",
    long_description=open("README.rst", "r").read(),
    name="marvelous",
    packages=find_packages(),
    url="http://github.com/rkuykendall/marvelous",
    version=version,
    zip_safe=True,
)
