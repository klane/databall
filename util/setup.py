from setuptools import setup

setup(
    name='nbprocess',
    version='0.1',
    py_modules=['nbprocess'],
    install_requires=[
        'Click',
        'PyYAML',
    ],
    entry_points='''
        [console_scripts]
        nbprocess=nbprocess:cli
    ''',
)
