from setuptools import setup, find_packages

setup(
    name="django-esewa",
    version="1.0.9",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests>=2.25.1",  
    ],
    description="A Django utility for eSewa signature generation.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Nischal Lamichhane",
    author_email="nischallc56@gmail.com",
    url="https://github.com/hehenischal/django-esewa",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Django",
        "Framework :: Flask",
        "Framework :: FastAPI",

        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",

        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.6",
)
