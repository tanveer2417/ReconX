from setuptools import setup, find_packages

setup(
    name='reconx',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'reconx = reconx.main:main',  # Calls the main() function from reconx/main.py
        ],
    },
    install_requires=[
        'requests',
        'dnspython',
        'python-whois',
        'colorama',
        'beautifulsoup4'
        'pyfiglet'
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
