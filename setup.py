#!/usr/bin/env python3

from setuptools import find_packages, setup

setup(
    name="visiology-py",
    packages=[
        *find_packages(include="visiology_py"),
        *find_packages(include="i2ls"),
    ],
    version="0.3.0",
    description=(
        "High level wrappers for Visiology APIs: "
        "Datacollection, ViQube and ViQube admin"
    ),
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://gitlab.com/polymedia-orv/orv/visiology-py",
    author="Denis <codingjerk> Gruzdev",
    author_email="codingjerk@gmail.com",
    license="MIT",

    install_requires=[],
    setup_requires=[
        "dataclasses==0.6",
        "funcy==1.15",
        "mypy==0.782",
        "pycodestyle==2.6.0",
        "pytest-cov==2.10.1",
        "pytest-runner==5.2",
        "pytest==6.0.1",
        "requests==2.24.0",
        "radon==4.3.2",
        "wheel==0.34.2",
    ],
    tests_require=[
        "mypy==0.782",
        "pycodestyle==2.6.0",
        "pytest-cov==2.10.1",
        "pytest-runner==5.2",
        "pytest==6.0.1",
        "radon==4.3.2",
    ],
    test_suite="tests",
)
