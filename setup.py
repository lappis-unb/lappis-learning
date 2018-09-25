from setuptools import setup, find_packages

setup(
    name='salic-ml-arch',
    version='0.0.1',
    description='Automate the Salic proposal admission process',
    url='https://github.com/lappis-unb/salic-ml',
    license='GPL v3.0',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=['flask', 'numpy', 'pandas', 'pyodbc', 'scipy'],
    python_requires='>=3',
    entry_points={
        'console_scripts': [
            'salicml = salicml.cli.main:main',
        ]
    },

)
