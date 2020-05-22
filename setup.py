import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = [
    "requests",
    "lxml",
]

packages = [
    "googleform",
    "googleform.questions",
]

setuptools.setup(
    name="googleform",
    version="0.0.1a2",
    author="Joel Tio",
    author_email="joeltiojinhon@gmail.com",
    description="Submit Google Forms with magic",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/joeltio/google-form-python",
    packages=packages,
    install_requires=requirements,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
