from setuptools import setup, find_packages

setup(
    name="api-hijacker",
    version="0.2.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.9.2",
        "cloudscraper @ git+https://github.com/VeNoMouS/cloudscraper.git@edef7647e76ff23a57653e9da6d540ad4e53d1a2"
    ],
    author="PolarisWater",
    author_email="",
    description="Create your own python library for interacting with any website's API.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/PolarisWater/api-hijacker",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.9",
)
