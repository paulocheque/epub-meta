#from distutils.core import setup
from setuptools import setup, find_packages

# http://guide.python-distribute.org/quickstart.html
# python setup.py sdist
# python setup.py register
# python setup.py sdist upload
# pip install epub_meta
# pip install epub_meta --upgrade --no-deps
# Manual upload to PypI
# http://pypi.python.org/pypi/epub_meta
# Go to 'edit' link
# Update version and save
# Go to 'files' link and upload the file

VERSION = '0.0.2'

tests_require = [
]

install_requires = [
]

# from pip.req import parse_requirements
# install_requires = parse_requirements('requirements.txt')
# tests_require = parse_requirements('requirements-dev.txt')

setup(name='epub_meta',
      url='https://github.com/pluralsight/epub-meta',
      author='Pluralsight',
      keywords='python epub metadata',
      description='',
      license='MIT',
      classifiers=[
          'Operating System :: OS Independent',
          'Topic :: Software Development',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: Implementation :: PyPy',
      ],

      version=VERSION,
      install_requires=install_requires,

      test_suite='tests',
      tests_require=tests_require,
      extras_require={'test': tests_require},

      packages=find_packages(),
)

