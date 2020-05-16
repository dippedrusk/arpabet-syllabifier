from pathlib import Path
import setuptools

pkg_root = Path(__file__).resolve().parent

with open(pkg_root.joinpath('README.md')) as f:
    long_description = f.read()

with open(pkg_root.joinpath('requirements.txt')) as f:
    requirements = [r.strip() for r in f.readlines()]

setuptools.setup(
    name='syllabifier',
    version='0.0.1',
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
