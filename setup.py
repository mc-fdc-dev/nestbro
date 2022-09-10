from setuptools import setup, find_packages


with open("requirements.txt", "r") as f:
    install_requires = f.readlines()

setup(
    name="nestbro",
    version="0.1.0",
    install_requires=install_requires,
    packages=find_packages()
)
