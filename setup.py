import setuptools


setuptools.setup(
    name="gomoku_ai",
    version="0.0.1",
    packages=setuptools.find_packages(),
    package_data={"": ["*"]},
    install_requires=[
        "tensorlayer==1.10.1",
        "tensorflow==1.12.0"
    ],
    python_requires=">=3.6",
)
