import setuptools

# read the description file 
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'doc/description.md'), encoding='utf-8') as f:
    long_description_text = f.read()

setuptools.setup(
    name="cinemasci",
    version="1.7.4",
    author="David H. Rogers",
    author_email="dhr@lanl.gov",
    description="Cinema scientific toolset.",
    long_description=long_description_text,
    long_description_content_type='text/markdown',
    url="https://github.com/cinemascience",
    include_package_data=True,
    packages=["cinemasci", 
                "cinemasci.cdb", 
                "cinemasci.cis",
                "cinemasci.viewers",
                "cinemasci.pynb",
                "cinemasci.install",
                "cinemasci.server"
            ],
    install_requires=[
        "pandas",
        "jupyterlab",
        "ipywidgets",
        "pyyaml",
        "scikit-image",
        "h5py",
        "matplotlib"
    ],
    scripts=['scripts/cisconvert', 'doc/description.md'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
)
