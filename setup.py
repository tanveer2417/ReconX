from setuptools import setup, find_packages

setup(
    name='reconx',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'reconx = reconx.main:main',  # Make sure this path is correct!
        ],
    },
    install_requires=[
        'termcolor'
        'tabulate'
        'requests'
        'googlesearch-python'
        'python-whois'
        'colorama'
        'urllib3'
        'beautifulsoup4'
        'tldextract'
        'dnspython'
        'selenium'
    ],
    author='Mariya Fareed, Ruheena Begum, Tanveer Fatima',
    description='Automated OSINT and Recon CLI tool',
    long_description=(
        'ReconX is a Python-based command-line tool for automating OSINT and reconnaissance tasks. '
        'It supports subdomain enumeration, metadata extraction, WHOIS, DNS, IP info lookup, '
        'GitHub dorks, and more.'
    ),
    long_description_content_type='text/markdown',
    url='https://github.com/tanveer2417/ReconX',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Information Technology',
        'Topic :: Security',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
