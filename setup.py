from setuptools import setup

setup(
    name='pylisten',
    version='0.0',
    description='Tools for analysing data from the listen software.',
    author='Dominic Ward',
    author_email='contactdominicward+github@gmail.com',
    url='https://github.com/deeuu/listen',
    packages=['pylisten'],
    license='MIT',
    install_requires=[
        'scipy >= 1.0.0',
        'numpy >= 1.12.1',
        'pandas >= 0.23.0',
        'matplotlib >= 2.0.0',
        'seaborn >= 0.9.0',
        'krippendorff >= 0.2.1',
        'six',
        'future',
    ],
)
