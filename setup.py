from distutils.core import setup


setup(
    name="runtime_typing",
    packages=["runtime_typing"],
    version="0.1.0",
    license="MIT",
    description="Checking typing type hints at runtime.",
    author="Jonathan Scholbach",
    author_email="j.scholbach@posteo.de",
    url="https://github.com/jonathan-scholbach/runtime_typing",
    download_url="https://github.com/jonathan-scholbach/runtime_typing/v_010.tar.gz",
    keywords=["typing", "validation", "validate"],
    install_requires=[],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
