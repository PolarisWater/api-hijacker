from setuptools import setup, find_packages

setup(
    name="apiCore",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.9.2",
        "cloudscraper>=1.2.70"
    ],
    author="PolarisWater",
    author_email="",
    description="Create your own python library for interacting with any website's API.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/PolarisWater/apiCore",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.9",
)
