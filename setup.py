import setuptools
import template_escape

setuptools.setup(name='template_project_escape',
                 version=template_escape.__version__,
                 description="DESCRIPTION",  # these should be minimum list of what is needed to run
                 packages=setuptools.find_packages(),
                 install_requires=['numpy'],
                 package_data={'template_project_escape': ['./template_project_escape/*']},
                 tests_require=['pytest'],
                 author='See Guidelines',
                 author_email='See Guidelines',
                 license='See LICENSE file',
                 url='https://gitlab.in2p3.fr/escape2020'
                 )
