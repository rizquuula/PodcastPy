"""
Created on Fri 02 15:03:00 2022
@license: MIT License
@author: eiproject (https://github.com/eiproject)

"""

from .podcastpy import PodcastPy


def auto_trimmer(original_video_path:str, result_video_path:str, time_margin_in_second=0.25, hist_sampling_data=50):
    """
    Auto trim video to remove audio noise and blank using PodcastPy

    #### Args:
        original_video_path (str): Original video to be processed
        result_video_path (str): Video result path
        time_margin_in_second (float, optional): Minimum time between the sound gap. Defaults to 0.25 seconds.
        hist_sampling_data (int, optional): Histogram sampling data, used on noise removal process. Defaults to 100.
    """
    app = PodcastPy()
    app.auto_trimmer(original_video_path, 
             result_video_path, 
             time_margin_in_second, 
             hist_sampling_data)