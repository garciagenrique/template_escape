#!/usr/bin/env python

import setuptools
import template_project_escape

# Define entry points for command-line scripts
entry_points = {'console_scripts': ['square_number = template_project_escape.code_template_escape:main']}

setuptools.setup(name='template_project_escape',
                 version=template_project_escape.__version__,
                 description="Template project for the ESCAPE repository",
                 packages=setuptools.find_packages(),
                 install_requires=['numpy'],
                 package_data={'template_project_escape': ['./template_project_escape/*']},
                 tests_require=['pytest'],
                 author='https://github.com/garciagenrique',
                 author_email='garcia<at>lapp.in2p3.fr',
                 license='Open Source. MIT license. See LICENSE file.',
                 url='https://gitlab.in2p3.fr/escape2020/wp3/template_project_escape',
                 entry_points=entry_points,
                 )  
