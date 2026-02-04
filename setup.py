#!/usr/bin/env python3
"""
AgentRouter - Setup Script

Intelligent task routing for Team Brain AI agents.
Routes tasks to optimal agents based on task type, cost, and speed.

Author: Atlas (Team Brain)
Date: January 18, 2026
License: MIT
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README for long description
readme_path = Path(__file__).parent / "README.md"
long_description = ""
if readme_path.exists():
    long_description = readme_path.read_text(encoding="utf-8")

setup(
    name="agentrouter",
    version="1.0.0",
    author="Atlas (Team Brain)",
    author_email="logan@metaphysicsandcomputing.com",
    description="Intelligent task routing for Team Brain AI agents",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DonkRonk17/AgentRouter",
    py_modules=["agentrouter"],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Distributed Computing",
    ],
    keywords="ai, agent, routing, task, team-brain, automation",
    entry_points={
        "console_scripts": [
            "agentrouter=agentrouter:main",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/DonkRonk17/AgentRouter/issues",
        "Source": "https://github.com/DonkRonk17/AgentRouter",
        "Documentation": "https://github.com/DonkRonk17/AgentRouter#readme",
    },
    license="MIT",
)
