"""Python setup.py for project_name package"""
import io
import os
from setuptools import find_packages, setup

setup(
    name="AccuWeather",
    version="0.0.1",
    description="project_description",
    url="https://github.com/Thomas1942/AccuWeather/",
    long_description="README.md",
    long_description_content_type="text/markdown",
    author="Thomas Libosan",
    install_requires="requirements.txt",
    entry_points={
        "console_scripts": ["project_name = project_name.__main__:main"]
    }
)