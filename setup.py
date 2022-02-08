from setuptools import setup
from podcastpy import __version__
import pathlib

BASE_DIR = pathlib.Path(__file__).parent
README = (BASE_DIR / "README.md").read_text()

setup(
    name="podcastpy",
    version=__version__,
    author="M Razif Rizqullah",
    author_email="razifrizqullah@gmail.com",
    url='https://github.com/eiproject/PodcastPy',
    description="PodcastPy - Python Tools for Podcast",
    long_description=README,
    long_description_content_type="text/markdown",
    license='MIT',
    packages=['podcastpy'],
    include_package_data=True,
    install_requires=[
                'tqdm',
                'numpy',
                'scipy',
                'matplotlib',
                'pydub',
            ],
    keywords=['python', 'glrlm', 'feature extraction', 'image processing'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)

# pip install --upgrade setuptools
# pip install wheel
# python setup.py sdist bdist_wheel
# twine upload --skip-existing dist/*