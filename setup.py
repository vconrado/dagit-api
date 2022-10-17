import os

from setuptools import find_packages, setup

readme = open('README.md').read()

install_requires = [
                    'click==7.1.2', 
                    'gql==2.0.0',
                    'pyyaml==6.0',
                    'mergedeep==1.3.4'
                    ]

packages = find_packages()

g = {}
with open(os.path.join('dagit_api', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['__version__']

setup(
    name='dagit_api',
    version=version,
    description=__doc__,
    long_description=readme,
    keywords=[],
    license='MIT',
    author='Vitor Gomes',
    author_email='vconrado@gmail.com',
    url='',
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=install_requires,
    classifiers=[],
    entry_points={
        'console_scripts': [
            'dagit_cli = dagit_api.cli:cli'
        ]
    }
)