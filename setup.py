from setuptools import setup, find_packages

setup(
    name="dankert-download",
    version="0.1.0",
    author="DanKert",
    author_email="dan.kert.official@gmail.com",
    description="Универсальный загрузчик медиа с платформ TikTok, YouTube, Instagram и др.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Dan-Kert/dankert-download",
    packages=find_packages(),
    install_requires=open("requirements.txt").read().splitlines(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "dankert-download = dankertdownload.main:main", 
        ]
    },
)
