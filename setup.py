import os

from setuptools import find_packages, setup

readme = open('README.rst').read()

install_requires = [
                    'click==7.1.2', 
                    'gql==2.0.0',
                    'pyyaml==6.0',
                    'mergedeep==1.3.4',
                    'dagster==0.14.0',
                    'protobuf==3.17.2',
                    'grpcio==1.39.0',
                    'grpcio-health-checking==1.39.0'
                    ]

packages = find_packages()

g = {}
with open(os.path.join('dagster_graphql_client', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['__version__']

setup(
    name='dagster_graphql_client',
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
            'dagster_client = dagster_graphql_client.cli:cli'
        ]
    }
)