"""
Setup script for OMNIMIND

The Autonomous, Self-Simulating, Self-Evolving Cognitive Kernel
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="omnimind",
    version="0.1.0",
    author="Priyanshu Mishra",
    author_email="your.email@example.com",
    description="The Autonomous, Self-Simulating, Self-Evolving Cognitive Kernel",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/omnimind",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "flake8>=6.1.0",
            "black>=23.0.0",
            "isort>=5.12.0",
        ],
        "dashboard": [
            "streamlit>=1.28.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "omnimind=main:app",
            "omnimind-test=run_omnimind:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.yml", "*.yaml"],
    },
) 