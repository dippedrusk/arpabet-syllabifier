import os
import pathlib
import setuptools

pkg_root = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(pkg_root, 'README.md')) as f:
    long_description = f.read()

with open(os.path.join(pkg_root, 'requirements.txt')) as f:
    requirements = [r.strip() for r in f.readlines()]

setuptools.setup(
    name='syllabifyARPA',
    version='0.0.1',
    description='syllabifyARPA will chunk your English ARPABET pronunciations into syllables',
    long_description=long_description,
    packages=setuptools.find_packages(exclude=('tests',)),
    python_requires='>= 3.5',
    install_requires=requirements,
    tests_require='pytest',
    author='Vasundhara Gautam',
    author_email='vasundhara131719@gmail.com',
    include_package_data=True,
    platforms='any',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
    ],
)
