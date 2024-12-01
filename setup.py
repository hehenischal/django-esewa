from setuptools import setup, find_packages

setup(
    name="django-esewa",
    version="0.1.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    description="A Django utility for eSewa signature generation.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="nischallc56@gmail.com",
    url="https://github.com/hehenischal/django-esewa",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Django",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.6",
)
