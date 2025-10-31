"""
Rowell Infra Python SDK Setup
Alchemy for Africa: Stellar + Hedera APIs & Analytics
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

# Read requirements
def read_requirements():
    requirements_path = os.path.join(os.path.dirname(__file__), "requirements.txt")
    if os.path.exists(requirements_path):
        with open(requirements_path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip() and not line.startswith("#")]
    return []

setup(
    name="rowell-infra-sdk",
    version="1.0.0",
    author="Rowell Infra Team",
    author_email="sdk@rowell-infra.com",
    description="Rowell Infra Python SDK - Alchemy for Africa (Stellar + Hedera APIs & Analytics)",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/rowell-infra/rowell-infra",
    project_urls={
        "Bug Reports": "https://github.com/rowell-infra/rowell-infra/issues",
        "Source": "https://github.com/rowell-infra/rowell-infra",
        "Documentation": "https://docs.rowell-infra.com",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Office/Business :: Financial",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "pre-commit>=3.0.0",
        ],
        "docs": [
            "sphinx>=6.0.0",
            "sphinx-rtd-theme>=1.2.0",
            "myst-parser>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "rowell=rowell_infra.cli:main",
        ],
    },
    keywords=[
        "stellar",
        "hedera",
        "blockchain",
        "africa",
        "fintech",
        "remittance",
        "stablecoin",
        "api",
        "sdk",
        "python",
    ],
    include_package_data=True,
    zip_safe=False,
)
