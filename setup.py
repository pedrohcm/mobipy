import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name='MobiPy',
    version="0.0.1",
    author='Pedro Maia',
      author_email='pedro.maia@ccc.ufcg.edu.br',
    description='A library for analyzing user mobility patterns',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='http://github.com/pedrohcm/mobipy',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7.16',
)