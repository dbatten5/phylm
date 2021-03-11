import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name='Phylm',
    version='0.1.1',
    description='Aggregrate useful data about films',
    long_description=README,
    long_description_content_type="text/markdown",
    author='Dom Batten',
    author_email='dominic.batten@googlemail.com',
    url = 'https://github.com/dbatten4/phylm',
    license="MIT",
    install_requires=[
        'beautifulsoup4',
        'requests',
        'imdbpy',
    ],
    packages=find_packages(),
)
