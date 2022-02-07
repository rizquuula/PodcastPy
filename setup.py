from setuptools import setup
import pathlib

BASE_DIR = pathlib.Path(__file__).parent
README = (BASE_DIR / "README.md").read_text()

setup(
    name="podcastpy",
    version="0.1.0",
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
            'certifi>=2021.10.8',
            'charset-normalizer>=2.0.11',
            'colorama>=0.4.4',
            'cycler>=0.11.0',
            'decorator>=4.4.2',
            'fonttools>=4.29.1',
            'idna>=3.3',
            'imageio>=2.14.1',
            'imageio-ffmpeg>=0.4.5',
            'kiwisolver>=1.3.2',
            'matplotlib>=3.5.1',
            'moviepy>=1.0.3',
            'numpy>=1.22.2',
            'packaging>=21.3',
            'Pillow>=9.0.1',
            'proglog>=0.1.9',
            'pydub>=0.25.1',
            'pyparsing>=3.0.7',
            'python-dateutil>=2.8.2',
            'requests>=2.27.1',
            'scipy>=1.7.3',
            'six>=1.16.0',
            'tqdm>=4.62.3',
            'urllib3>=1.26.8'
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
# twine upload dist/*