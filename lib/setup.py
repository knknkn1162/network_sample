from setuptools import setup, find_packages

setup(
    name='cmlmag',
    version='0.1',
    install_requires=[
      "virl2_client[pyats]",
      "pyats[full]",
      "python-dotenv",
    ],
    packages=find_packages()
)