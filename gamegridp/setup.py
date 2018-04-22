from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))


# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
	long_description = f.read()

setup(
  name = 'gamegridp',
  version = '0.3.0.4',
  description = 'A gamegrid clone for python',
  long_description=long_description,
  long_description_content_type='text/markdown', 
  author = 'Andreas Siebel',
  author_email = 'andreas.siebel@it-teaching.de',
  keywords = ['game', 'education'], # arbitrary keywords
  url = 'https://github.com/asbl/gamegridp', # use the URL to the github repo
  download_url = 'https://github.com/asbl/gamegridp/archive/master.zip', # I'll explain this in a second
  license="MIT",
  classifiers = ['Development Status :: 3 - Alpha',],
  packages=find_packages(exclude=['contrib', 'docs', 'tests']), # Required
  package_data={'gamegridp': ['data/*.png']},
  install_requires=['pygame'],
)