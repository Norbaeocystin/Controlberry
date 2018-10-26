import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="controlberry_pkg",
    install_requires=["pymongo","Adafruit_DHT"],
    version="0.0.1",
    author="Rastislav_Baran",
    author_email="baranrastislav@gmail.com",
    description="Package which needs to be installed on Raspberry Pi 3 to control Raspberry Pi 3 by MongoDB ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_data={'Controlberry': ['*.json']},
    entry_points={'console_scripts':['controlberry = Controlberry.control']},
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

 
