import os
import setuptools

pkg_root = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(pkg_root, 'README.md'), 'r', encoding='utf-8') as f:
    long_description = f.read()

with open(os.path.join(pkg_root, 'requirements.txt'), 'r', encoding='utf-8') as f:
    requirements = [r.strip() for r in f.readlines()]

with open(os.path.join(pkg_root, 'VERSION'), 'r', encoding='utf-8') as f:
    VERSION = f.read().strip()

setuptools.setup(
    name='syllabifier',
    version=VERSION,
    description='syllabifier chunks your English ARPABET pronunciations into syllables',
    long_description=long_description,
    packages=setuptools.find_packages(where='src', exclude=('tests',)),
    package_dir={'': 'src'},
    python_requires='>= 3.5',
    setup_requires=requirements,
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
