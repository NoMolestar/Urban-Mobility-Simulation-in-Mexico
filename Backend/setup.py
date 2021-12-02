"""
Hello World app for running Python apps on Bluemix
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="Intersection Simulation",
    version="1.0.0",
    description="Simulation of a busy intersection with computational agents.",
    long_description=long_description,
    url="https://github.com/IBM-Bluemix/python-hello-world-flask",
    license="Apache-2.0",
)
