# setup.py

from setuptools import setup, find_packages

setup(
    name="readSortAI",            # The name of your package
    version="1.2.0",                    # Version number
    packages=find_packages(),           # Automatically find packages in the repository
    install_requires=[                  # List your package dependencies here
        "requests",
    ],
    author="Michael Monefeldt",
    author_email="michaelmonefeldt@gmail.com",
    description="A package to interact with the OpenAI API for image processing.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/your_username/openai_api_tools",  # Replace with your GitHub URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Update if you use a different license
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)