from setuptools import setup, find_packages

setup(
    name='reconx',
    version='1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'reconx=reconx.main:main',
        ],
    },
    install_requires=[
        'requests',
        'dnspython',
        'python-whois'
    ],
    author='Mariya Fareed',
    description='Automated OSINT and Recon CLI tool',
    long_description='A Python tool to automate OSINT tasks such as Google/GitHub dorks, metadata extraction, WHOIS, DNS, IP info, and more.',
    long_description_content_type='text/markdown',
    url='https://github.com/mariyafareed/reconx',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
