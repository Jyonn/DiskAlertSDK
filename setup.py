from setuptools import setup, find_packages

setup(
    name='DiskAlertSDK',
    version='0.0.1',
    keywords=['django'],
    description='fast Django app development',
    long_description='field validation detector, model advanced search, unified error class',
    license='MIT Licence',
    url='https://github.com/Jyonn/SmartDjango',
    author='Jyonn Liu',
    author_email='i@6-79.cn',
    platforms='any',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
)