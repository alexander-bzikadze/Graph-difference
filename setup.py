from codecs import open
from os import path

from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='graph_diff',
      version='0.1.0',
      description='Package providing series of algorithms to solve graph difference problem',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/alexander-bzikadze/graph_diff',
      author='Aleksandr Bzikadze',
      author_email='alexander.bzikadze@gmail.com',
      classifiers=['Development Status :: 3 - Alpha',
                   'Intended Audience :: Developers',
                   # 'Topic :: Computer Science :: Graph Problems',
                   # 'License :: Apache License 2.0',
                   'Programming Language :: Python :: 3.6'],
      keywords='graph difference nirvana yandex',
      packages=find_packages(exclude=['docs',
                                      'graph_diff',
                                      'tests']),
      install_requires=['numpy',
                        'stringcase',
                        'pydot',
                        'cppimport'],
      project_urls={'Bug Reports': 'https://github.com/alexander-bzikadze/graph_diff/issues',
                    'Say Thanks!': 'https://saythanks.io/to/alexander-bzikadze',
                    'Source': 'https://github.com/alexander-bzikadze/graph_diff'})
