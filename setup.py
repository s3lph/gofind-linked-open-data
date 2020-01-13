
from setuptools import setup, find_packages

from untitled_project import __version__


setup(
    name='untitled_project',
    version=__version__,
    author='s3lph',
    author_email='',
    description='',
    license='MIT',
    keywords='tourism,gofind,linked data,open data,linked open data',
    url='https://github.com/s3lph/untitled-linked-open-data-project',
    packages=find_packages(exclude=['*.test']),
    long_description='',
    python_requires='>=3.6',
    install_requires=[
        'bottle',
        'mysql-connector-python',
        'lxml',
        'connexion',
        'connexion[swagger-ui]'
    ],
    entry_points={
        'console_scripts': [
            'server = untitled_project.server:main'
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Bottle',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application'
    ]
)
