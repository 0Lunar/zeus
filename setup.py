from setuptools import setup, find_packages


setup(
    name="zeus",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        "colorama>=0.4.6",
        "python-nmap==0.7.1",
        "requests>=2.25.1",
        "urllib3>=1.26.5",
        "paramiko>=3.4.1",
        "regex>=2022.10.31"
    ],
    author="0lunar",
    author_email="LunarStone292@proton.me",
    description="Penetration Testing Framework",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/0lunar/zeus",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)