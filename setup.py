from setuptools import setup, find_packages

setup(
    name="factest",
    version="0.0.1",
    keywords=("pip", "factest", "alpha factor", "quant"),
    description="",
    long_description="A Fantistic Factor Analysising Tools For Quant",
    license="MIT Licence",

    url="https://github.com/zzb610/factest",
    author="zzb610",
    author_email="bwyuchi@163.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=["requirements.txt"]
)
