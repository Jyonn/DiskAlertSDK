from setuptools import setup, find_packages

setup(
    name='DiskAlertSDK',
    version='0.0.1',
    keywords=['disk', 'alert'],
    description='DiskAlert SDK',
    long_description='for LabDiskAlert',
    license='MIT Licence',
    url='https://github.com/Jyonn/DiskAlertSDK',
    author='Jyonn Liu',
    author_email='i@6-79.cn',
    platforms='any',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
)
