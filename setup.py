"""Setup script for options_bot package."""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="options_bot",
    version="1.0.0",
    author="Options Bot Team",
    description="Automated options trading ideas generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/options_bot",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "options-bot-scan=options_bot.runner.scan:run_scan",
            "options-bot-scheduler=options_bot.runner.scheduler:start_scheduler",
        ],
    },
)

