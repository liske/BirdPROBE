from setuptools import setup, find_packages
from datetime import date
from packaging import version as packaging_version
from platform import python_version

def readme():
    with open("README.md") as f:
        return f.read()

def version():
    with open("birdprobe/__init__.py") as fd:
        for line in fd:
            if line.startswith('__version__'):
                delim = '"' if '"' in line else "'"
                return line.split(delim)[1]

    raise RuntimeError("Unable to find version string.")

def install_requires():
    requires = [
        "birdnetlib>=0.5.1",
        "librosa",
        "resampy",
        "pyaudio"
    ]

    # Python 3.11 wheels for tflite-runtime are not available, yet:
    #   https://github.com/tensorflow/tensorflow/issues/60115
    #
    # Use tensorflow as a fallback.
    if packaging_version.parse(python_version()) >= packaging_version.parse("3.11"):
        requires += ["tensoflow"]
    else:
        requires += ["tflite-runtime>=2.12.0"]
    return requires


setup(
    name="birdprobe",
    version=version(),
    description="Detects birds from live recording based on birdnetlib.",
    author="Thomas Liske",
    author_email="thomas@fiasko-nw.net",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://codeberg.net/liske/birdprobe",
    license="AGPL3+",
    packages=find_packages(),
    install_requires=install_requires(),
    extras_require={
        'gps': [
            'gps'
        ],
        'pixelring': [
            'pixel_ring'
        ]
    },
    entry_points={
        "console_scripts": [
            "birdprobe-detector = birdprobe.birdnet:main",
            "birdprobe-location = birdprobe.location:main",
        ]
    },
)
