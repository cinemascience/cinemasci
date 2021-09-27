import setuptools

# read the description file 
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'description.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="cinemasci",
    version="1.5.4",
    author="David H. Rogers",
    author_email="dhr@lanl.gov",
    description="Cinema scientific toolset.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/cinemascience",
    include_package_data=True,
    package_data={'cinemasci': ['license.md', 'description.md']},
    packages=setuptools.find_packages(),
    install_requires=[
        "pandas",
        "jupyterlab",
        "ipywidgets",
        "pyyaml",
        "scikit-image",
        "h5py"
    ],
    scripts=['scripts/cisconvert'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
)
