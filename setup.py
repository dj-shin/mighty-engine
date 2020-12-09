import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mighty-dj-shin", # Replace with your own username
    version="0.0.1",
    author="DongJin Shin",
    author_email="dongjin.shin.00@gmail.com",
    description="Mighty card game engine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dj-shin/mighty-engine",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
