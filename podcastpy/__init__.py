"""
Created on Fri 02 15:03:00 2022
@license: MIT License
@author: eiproject (https://github.com/eiproject)

"""

from .podcastpy import PodcastPy


def auto_trimmer(original_video_path, result_video_path, time_margin_in_second=0.25, hist_sampling_data=50):
    app = PodcastPy()
    
    app.main(original_video_path, 
             result_video_path, 
             time_margin_in_second, 
             hist_sampling_data)