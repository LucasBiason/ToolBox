from setuptools import setup

setup(
    name='toolbox',
    version='1.0.1',
    descriptions='Toolbox library for projects',
    author='Lucas Biason',
    packages=[
        'toolbox',
    ],
    install_requires=[
        'pycpfcnpj==1.5.1',
        'validators==0.18.1',
    ]
)
