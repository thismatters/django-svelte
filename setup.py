from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="django-svelte",
    author="Paul Stiverson",
    url="https://github.com/thismatters/django-svelte/",
    version="0.2.1",
    packages=find_packages(exclude=("tests", "demo_project")),
    license="MIT",
    description="Facilitates adding Svelte frontend to Django",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.8",
    include_package_data=True,
    install_requires=[
        "Django>=3.2.0",
        "django-appconf>=1.0.0",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.1",
        "Framework :: Django :: 4.2",
        "Framework :: Django :: 5.0",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
)
