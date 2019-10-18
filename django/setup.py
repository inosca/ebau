"""Setuptools package definition."""

from setuptools import find_packages, setup

version = {}
with open("camac/camac_metadata.py") as fp:
    exec(fp.read(), version)


setup(
    name=version["__title__"],
    version=version["__version__"],
    author=version["__author__"],
    author_email=version["__email__"],
    description=version["__description__"],
    url=version["__url__"],
    packages=find_packages(),
)
