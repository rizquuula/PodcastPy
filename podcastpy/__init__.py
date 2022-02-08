"""
Created on Fri 02 15:03:00 2022
@license: MIT License
@author: eiproject (https://github.com/eiproject)

"""

from .podcastpy import PodcastPy
from .version import __version__


def auto_trimmer(
    original_media_path:str, 
    result_media_path:str, 
    time_margin_in_second:float=0.25, 
    noise_sampling_level:int=100):
    """
    Auto trim media to remove audio noise and blank using PodcastPy
    Media supported format: wav, aac, m4a, mp3, mp4, H.264, etc. (FFMPEG supported formats)

    #### Args:
        original_media_path (str): Original media to be processed
        result_media_path (str): Media result path
        time_margin_in_second (float, optional): Minimum time between the sound gap. Defaults to 0.25 seconds.
        noise_sampling_level (int, optional): Histogram sampling level, used on noise removal process. Defaults to 100.
    """
    app = PodcastPy()
    
    is_error = app.ffmpeg.is_media_supported(original_media_path)
    if not is_error: 
        app.auto_trimmer(original_media_path, 
             result_media_path, 
             time_margin_in_second, 
             noise_sampling_level)