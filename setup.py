from setuptools import setup, find_packages

PACKAGE = 'fixedwidthpy'
VERSION = '1.1.3'
AUTHOR = 'VoxLight'
AUTHOR_EMAIL = 'VoxLight@protonmail.com'
REPO_URL = 'https://github.com/VoxLight/fwf'
DESCRIPTION = 'Fixed Width Files are a NIGHTMARE!!... So, I took my time to make the BEST library for dealing with them! '
KEYWORDS = [
    'fixed width file',
    'fixed width file handler',
    'fixed width alternative',
    'fixed width columns',
    'fixed width rows',
]
setup(
    name=PACKAGE,
    version=VERSION,
    packages=find_packages(),
    extras_require={
        'dev': [
            'pytest',
        ]
    },
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    license='Apache 2.0',
    keywords=KEYWORDS,
    url=REPO_URL,
    project_urls={
        'Bug Tracker': f'{REPO_URL}/issues',
        'Documentation': f'{REPO_URL}/blob/main/README.md',
        'Source Code': REPO_URL,
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
    python_requires='>=3.12',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
