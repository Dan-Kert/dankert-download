from setuptools import setup, find_packages

setup(
    name='dankert-download',
    version='0.1.0',
    author='DanKert',
    author_email='dan.kert.official@gmail.com', 
    description='Мощный загрузчик видео от DanKert, альтернатива yt-dlp',
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Dan-Kert/dankert-download',
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.7',
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'dankert_download = dankert_download.__main__:main'
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
