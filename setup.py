#!/usr/bin/env python3

from setuptools import find_packages, setup

setup(
    name="visiology-py",
    packages=find_packages(include="visiology_py"),
    version="0.1.0",
    description="High level wrappers for Visiology APIs: Datacollection, ViQube and ViQube admin",
    author="Denis <codingjerk> Gruzdev",
    license="MIT",

    install_requires=[],
    setup_requires=[
        "pytest==6.0.1",
        "pytest-runner==5.2",
        "pytest-cov==2.10.1",
        "pycodestyle==2.6.0",
        "mypy==0.782",
        "wheel==0.34.2",
    ],
    tests_require=[
        "pytest==6.0.1",
        "pytest-runner==5.2",
        "pytest-cov==2.10.1",
        "pycodestyle==2.6.0",
        "mypy==0.782",
    ],
    test_suite="tests",
)