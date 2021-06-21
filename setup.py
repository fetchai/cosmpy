from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='cosm',
    version='0.0.1',
    description='A library for writing tools to interact with cosmos networks',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/fetchai/pycosm',
    author='Ed FitzGerald',
    author_email='edward.fitzgerald@fetch.ai',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
    ],

    keywords='cosmos, gaia, fetchhub, fetchai',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.6, <4',
    install_requires=['ecdsa', 'bech32'],
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage', 'pytest', 'tox'],
    },
    project_urls={
        'Bug Reports': 'https://github.com/fetchai/pycosm/issues',
        'Source': 'https://github.com/fetchai/pycosm',
    },
)