from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='FoshIot',
      version=version,
      description="Small wrapper for Dialog IoT development kit",
      long_description="""
        It is too hard if someone wants to develop application with this IoT module
        without any experiance of mobile programming and so on. 
        For better underestandign of this wrapper library please read Readme and 
        Iot datasheet. """,
      classifiers=[],
      keywords='IoT, Dialog Semiconductor, da14583, ble',
      author='Michal Sladecek',
      author_email='misisnik@gmail.com',
      url='',
      license='GPLv3',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'pygatt'
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
