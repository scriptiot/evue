import setuptools

with open("README-pypi.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="evue",
    version="0.1.6.1",
    author="dragondjf",
    author_email="ding465398889@163.com",
    description="Evue is a high-performance gui framework base an html/css which can run on windows/linux/macos/ios/andriod/rtos! Write once, run everywhere! ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/scriptiot/evm",
    packages=setuptools.find_packages(),
    install_requires=[
        "flet==0.3.2",
        "pyee>=9.0.4",
        "loguru>=0.6.0",
        "pyperclip>=1.8.2",
        "pillow>=9.3.0",
        "qrcode>=7.3.1",
    ],
    extras_require={
        'dev': []
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 3'
    ],
    python_requires='>=3.7',
)
