# File: setup.py
from setuptools import setup, find_packages

setup(
    name="my_rate_limiter",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "flask",
        # Add other dependencies like redis if you implement a RedisCache
    ],
    author="Sameet Naik",
    author_email="sameetfe@gmail.com",
    description="A lightweight API rate limiter for FastAPI and Flask",
    url="https://github.com/Sameet93/my_rate_limiter",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Flask",
        "Framework :: FastAPI",
    ],
)

