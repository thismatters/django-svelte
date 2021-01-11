from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="django-svelte",
    author="Paul Stiverson",
    url="https://github.com/thismatters/django-svelte/",
    version="0.1.3",
    packages=["django_svelte"],
    license="MIT",
    description="Facilitates adding Svelte frontend to Django",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.7.4",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Framework :: Django :: 3.1",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
)
