from podcastpy import auto_trimmer

# a place where your original video stored
ORIGINAL_PATH = "240.mp4"

# a desired path where your result video will saved
RESULT_PATH = "after.mp4"

# margin for trim video, so there is no sudden cut or trim
TIME_MARGIN = 0.25

# number of how many bars in the histogram
NOISE_SAMPLING_DATA = 50

auto_trimmer(original_video_path=ORIGINAL_PATH,
     result_video_path=RESULT_PATH,
     time_margin_in_second=TIME_MARGIN,
     hist_sampling_data=NOISE_SAMPLING_DATA)
