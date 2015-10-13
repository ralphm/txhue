#!/usr/bin/env python

from setuptools import setup

setup(name='txhue',
      version='0.0.0',
      description='Asynchronous client library to Philips Hue',
      author='Ralph Meijer',
      author_email='ralphm@ik.nu',
      maintainer_email='ralphm@ik.nu',
      url='https://github.com/ralphm/txhue',
      license='MIT',
      platforms='any',
      packages=[
          'txhue',
          'txhue.test',
      ],
      install_requires=[
          'Twisted',
          'treq',
      ],
)
