from setuptools import setup, find_packages

setup(
    name="bisheng",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "sqlmodel",
        # other dependencies...
    ],
)
