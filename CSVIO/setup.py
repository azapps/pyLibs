#!/usr/bin/env python

from setuptools import setup

setup(
        name='CsvIO',
        version='0.1',
        description='Easy reading and writing from/to CSV-Files',
        author='Anatolij Zelenin',
        author_email='az@azapps.de',
        url='https://github.com/azapps/pyLibs',
        packages=['CsvIO'],
        long_description="""Read and Write from/to a CSV-file It automatically infers the format of the given file and converts it to an array. Write to the file in the given format.""",
        license='MIT',
        install_requires=['setuptools']
        )
