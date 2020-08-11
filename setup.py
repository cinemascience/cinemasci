import setuptools

setuptools.setup(
    name="cinemasci",
    version="0.1",
    author="David H. Rogers",
    author_email="dhr@lanl.gov",
    description="Tools for the Cinema scientific toolset.",
    url="https://github.com/cinemascience",
    packages=["cinemasci", 
                "cinemasci.cdb", 
                "cinemasci.cis",
                "cinemasci.cis.read",
                "cinemasci.cis.write"
            ],
    install_requires=[
        "pandas",
        "pillow",
        "h5py"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD",
        "Operating System :: OS Independent",
    ],
)
