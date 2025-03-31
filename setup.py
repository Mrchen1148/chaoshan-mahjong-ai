from setuptools import setup, find_packages

setup(
    name="chaoshan_mahjong_ai",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.21.0",
        "tqdm>=4.65.0",
    ],
    author="ChaoshanMJ Team",
    author_email="contact@example.com",
    description="An intelligent Chaoshan Mahjong AI plugin",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
