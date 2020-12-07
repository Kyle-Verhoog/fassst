from setuptools import setup


with open("README.md", "r") as f:
    long_description = f.read()


setup(
    name="fassst",
    description="helps make your python go fast",
    url="https://github.com/Kyle-Verhoog/fassst",
    author="Patrick Gingras <775.pg.12@gmail.com>, Kyle Verhoog <kyle@verhoog.ca>",
    author_email="775.pg.12@gmail.com, kyle@verhoog.ca",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="Apache 2",
    packages=["fassst"],
    package_dir={
        "fassst": "src",
    },
    python_requires=">=3.8",
    install_requires=[],
    setup_requires=["setuptools_scm"],
    use_scm_version=True,
)
