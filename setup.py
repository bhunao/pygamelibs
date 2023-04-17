from setuptools import setup, find_packages

README = open("readme.md").read()
setup(
    name="pygamelibs",
    version="0.0.0",
    author="Bruno Félix",
    description="stuff for game/simulation development.",
    long_description=README,
    url="https://github.com/bhunao/pygamelibs/",
    packages=find_packages(exclude=("test*"))
)