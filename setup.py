from setuptools import setup, find_packages

setup(
    name='salic-ml-arch',
    version='0.0.1',
    description='Automate the Salic proposal admission process',
    url='https://github.com/lappis-unb/salic-ml',
    license='GPL v3.0',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=[
        'ipdb==0.11', 'ipython==6.5.0', 'numpy==1.15.1', 'pandas==0.23.4', 'pytest==3.8.0'
    ],
    python_requires='>=3',
)
