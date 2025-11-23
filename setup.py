"""Setup configuration for yahoo_fantasy_mcp package."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="yahoo_fantasy_mcp",
    version="0.1.0",
    author="Matt Spilchen",
    author_email="matt.spilchen@gmail.com",
    description="MCP server for Yahoo Fantasy Sports API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/yahoo_fantasy_mcp",
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "yahoo_fantasy_api>=2.0.0",
        "mcp>=0.1.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "isort>=5.12.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "yahoo-fantasy-mcp=yahoo_fantasy_mcp.__main__:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
