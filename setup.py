#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from setuptools import setup

def get_long_description():
    """
    Return the README.
    """
    return open("README.md", "r", encoding="utf8").read()


def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [
        dirpath
        for dirpath, dirnames, filenames in os.walk(package)
        if os.path.exists(os.path.join(dirpath, "__init__.py"))
    ]


env_marker_cpython = (
    "sys_platform != 'win32'"
    " and (sys_platform != 'cygwin'"
    " and platform_python_implementation != 'PyPy')"
)

env_marker_win = "sys_platform == 'win32'"
env_marker_below_38 = "python_version < '3.8'"

minimal_requirements = [
    "click==8.1.3",
    "colorama==0.4.6",
    "PyYAML==6.0",
    "pyinstaller==5.7.0",
    "pyinstaller-hooks-contrib==2022.15",
    "schedule==1.1.0",
    "windows-toasts==0.3.3",
    "winsdk==1.0.0b7"
]


extra_requirements = [
]


setup(
    name="Punctual",
    version="0.0.1",
    url="https://github.com/camratchford/punctual",
    license="CC0 1.0 Universal",
    description="Better task scheduler in Windows OS",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Cam Ratchford",
    author_email="cameron@ratchfordconsulting.com",
    packages=get_packages('punctual'),
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=minimal_requirements,
    extras_require={"standard": extra_requirements},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Administrators",
        "License :: MIT License",
        "Programming Language :: Python :: 3"
    ],
    entry_points={
        'console_scripts': {
            'punc = punctual.cli:run',
        }
    },
    project_urls={
        "Funding": "https://github.com/sponsors/camratchford",
        "Source": "https://github.com/camratchford/punctual",
        "Changelog": "https://github.com/camratchford/punctual/blob/master/CHANGELOG.md",
    },
)