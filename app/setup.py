"""
Setup script for packaging and distributing the project.

This script uses setuptools to package the project, including metadata
such as the project name, version, author, license, and dependencies.

Usage:
    To install the package, run:
        python setup.py install

    To create a source distribution, run:
        python setup.py sdist

    To create a wheel distribution, run:
        python setup.py bdist_wheel

Attributes:
    name (str): The name of the package.
    version (str): The current version of the package.
    author (str): The author's name.
    author_email (str): The author's email address.
    description (str): A brief description of the package.
    long_description (str): A detailed description of the package.
    long_description_content_type (str): The format of the long description (e.g., 'text/markdown').
    url (str): The URL for the package's homepage.
    packages (list): A list of all Python import packages that should be included in the package distribution.
    install_requires (list): A list of package dependencies.
    classifiers (list): A list of classifiers that provide metadata about the package.
"""

from __version__ import __version__
from setuptools import find_packages, setup

setup(
    name="hivebox",
    version=__version__,
    author="Cătălin Topală",
    description="In this DevOps end-to-end hands-on project, we will utilize the technology and open-source software to build an API to track the environmental sensor data from openSenseMap, a platform for open sensor data in which everyone can participate.",
    license="MIT",
    url="https://github.com/catalintopala/test-hivebox",
    packages=find_packages(),
)
