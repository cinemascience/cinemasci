import setuptools

setuptools.setup(
    name="cinemas",
    version="1.0",
    author="David H. Rogers",
    author_email="dhr@lanl.gov",
    description="Tools for the Cinema scientific toolset.",
    url="https://github.com/cinemascience",
    packages=["cinemas", 
                "cinemas.cdb", 
                "cinemas.cis",
                  "cinemas.cis.read",
                  "cinemas.cis.write"
            ],
    install_requires=[
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: BSD",
        "Operating System :: OS Independent",
    ],
)
