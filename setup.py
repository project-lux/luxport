from setuptools import setup, find_packages

setup(
    name="luxport",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
        "tqdm>=4.62.0",
        "jsonschema>=4.0.0",
    ],
    entry_points={
        'console_scripts': [
            'luxport=luxport.cli:main',
        ],
    },
    author="William J.B. Mattingly",
    description="A utility for exporting IIIF manifest data to ZIP files",
    keywords="iiif, manifest, export, yale, library",
    python_requires=">=3.7",
) 