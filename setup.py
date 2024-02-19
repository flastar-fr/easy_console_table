from setuptools import find_packages, setup


with open("app/README.md", "r") as f:
    long_description = f.read()

setup(
    name="easy-console-table",
    version="0.0.1",
    description="Simple package to create console table",
    package_dir={"": "easy_console_table"},
    packages=find_packages(where="easy_console_table"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/flastar-fr/easy_console_table",
    author="flastar",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    extras_require={
        "dev": ["pytest>=7.0", "twine>=4.0.2"],
    },
    python_requires=">=3.10",
)
