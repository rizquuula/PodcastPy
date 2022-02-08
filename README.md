# PodcastPy

Podcast Helper Tool in Python

![PyPI - License](https://img.shields.io/pypi/l/podcastpy)
![GitHub top language](https://img.shields.io/github/languages/top/eiproject/PodcastPy)
![GitHub all releases](https://img.shields.io/github/downloads/eiproject/PodcastPy/total)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/eiproject/podcastpy)

## Description

**Podcast** is something that we usually hear or watch, fill our warm and relax time. Sometimes podcasters find that it is difficult to manage time to create content and process it for a *ready to hear* product. `PodcastPy` is an open-source program aimed at solving the basic and recurring problems that often occur in podcast creation.

## Installation

```console
pip install podcastpy
```

PyPi link: <https://pypi.org/project/podcastpy>

## Usage Example

```python
from podcastpy import auto_trimmer

# a place where your original video stored
ORIGINAL_PATH = "original.mp4"

# a desired path where your result video will saved
RESULT_PATH = "result.mp4"

# margin for trim video, so there is no sudden cut or trim
TIME_MARGIN = 0.50

# number of how many bars in the histogram
NOISE_SAMPLING_LEVEL = 100

auto_trimmer(original_media_path=ORIGINAL_PATH,
     result_media_path=RESULT_PATH,
     time_margin_in_second=TIME_MARGIN,
     noise_sampling_level=NOISE_SAMPLING_LEVEL)

```

## Support

Reach me out on [Email](mailto:razifrizqullah@gmail.com "razifrizqullah@gmail.com")

## Contribution

If you find out this library as useful please give it a star to let everyone know.
If you have idea on how to improve this library, I am always open for every contributors. Thank you!

## Copyright

MIT License

Copyright (c) 2021 Muhammad Razif Rizqullah
