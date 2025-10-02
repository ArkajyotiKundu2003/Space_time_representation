from setuptools import setup, find_packages

setup(
    name="spacetime_process",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "networkx>=2.8",
        "matplotlib>=3.5",
        "numpy>=1.23",
        "pytest>=7.0",
    ],
    python_requires=">=3.8",
    author="Your Name",
    description="A framework for analyzing process embeddings in spacetime",
)