from setuptools import setup, find_packages

setup(
    name='dankert-download',
    version='0.1.0',
    description='dankert-download',
    author='dankert',
    packages=find_packages(),
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'dankert-download = dankert_install.__main__:main',
        ],
    },
)
