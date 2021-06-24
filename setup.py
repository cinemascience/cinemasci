import setuptools

setuptools.setup(
    name="cinemasci",
    version="1.5",
    author="David H. Rogers",
    author_email="dhr@lanl.gov",
    description="Cinema scientific toolset.",
    url="https://github.com/cinemascience",
    include_package_data=True,
    packages=["cinemasci", 
                "cinemasci.cdb", 
                "cinemasci.cis",
                "cinemasci.viewers",
                "cinemasci.pynb",
                "cinemasci.server"
            ],
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
