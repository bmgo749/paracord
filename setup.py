from setuptools import setup, find_packages

setup(
    name="paracord",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "para=paracord.cli:main"
        ]
    }
)