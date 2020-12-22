from setuptools import setup, find_packages

install_reqs = [
    'matplotlib>=1.4.0',
    'numpy>=1.9.1',
    'pandas>=0.18.0',
    'scipy>=0.14.0',
    'seaborn>=0.6.0',
    'statsmodels>=0.6.1',
    'IPython>=3.2.3',
    'empyrical>=0.5.0',
    'statsmodels',
    'tables',
]

setup(
    name="factest",
    version="0.0.8",
    keywords=["pip", "factest", "alpha factor", "quant"],
    description="",
    long_description="A Fantistic Factor Analysising Tools For Quant",
    license="MIT Licence",

    url="https://github.com/zzb610/factest",
    author="zzb610",
    author_email="bwyuchi@163.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=install_reqs
)
