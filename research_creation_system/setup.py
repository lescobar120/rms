from setuptools import setup, find_packages

setup(
    name="research-creation-system",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "python-docx", 
        "requests",
        # your other dependencies
    ],
    python_requires=">=3.8",
)