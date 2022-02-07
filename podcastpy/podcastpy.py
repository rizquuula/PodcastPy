"""
Created on Fri 02 15:03:00 2022
@license: MIT License
@author: eiproject (https://github.com/eiproject)

"""
import subprocess
import shutil
from pydub import AudioSegment
from moviepy.editor import VideoFileClip
import os
import csv
import time
import scipy.io.wavfile
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

class PodcastPy:
    """
    Podcast Tool in Python
    @author: M Razif Rizqullah (https://github.com/eiproject)
    """
    def __init__(self):
        self.__title__ = 'PodcastPy'
        self.__description__ = 'Podcast Automation Tools'
        self.__original_video_path = None
        self.__wav_audio_path = None
        self.__result_video_path = None
        self.__temp_dir = 'temp_'
        self.__temp_vid_result_metadata = 'temp_/temp_videos_metadata.txt'
        
    def __open_video_file(self):
        '''Open audio from video file using pydub'''
        sound = AudioSegment.from_file(self.__original_video_path)
        return sound    
    
    def __extract_audio_raw_data(self):
        '''Extract the audio to a .wav file'''
        self.__wav_audio_path = os.path.join(
            self.__temp_dir, os.path.splitext(os.path.basename(self.__original_video_path))[0] + '.wav') 
        
        AudioSegment.from_file(self.__original_video_path).export(self.__wav_audio_path, format='wav')

        # read wav file using scipy
        rate, audData = scipy.io.wavfile.read(self.__wav_audio_path)

        # if stereo grab both channels
        if audData.shape[1] > 1:
            channel1 = audData[:, 0]  # left
            channel2 = audData[:, 1]  # right
        
        # if mono
        else:  
            channel1 = audData[:, 0]
            channel2 = []

        time_tick = np.arange(0, float(audData.shape[0]), 1) / rate
        return channel1, channel2, time_tick
    
    
    def __noise_threshold_process(self, channel1, channel2, sampling_data, time_tick):
        '''Remove noise using histogram operation'''
        # concat stereo to mono
        channel_concat = np.int32(np.mean(np.array([np.int32(channel1), np.int32(channel2)]), axis=0)) \
            if channel2 != [] else np.int32(channel1)

        # # stereo plot
        # plt.figure(1)
        # plt.plot(time_tick, channel1, linewidth=0.05, alpha=1, color='#0000ff')
        # plt.plot(time_tick, channel2, linewidth=0.05, alpha=1, color='#ff0000')

        # # histogram plot
        # plt.figure(2)
        counts, bins, bars = plt.hist(np.abs(channel_concat), bins=sampling_data * 2)

        # finding threshold value
        threshold_val = bins[sampling_data + 1]
        
        # remove value below threshold
        channel_noise_removed = np.int32(
            np.where((-threshold_val < channel_concat) & (channel_concat < threshold_val), 
                     0, 
                     channel_concat))

        # # noise removed plot
        # plt.figure(3)
        # plt.plot(time_tick, channel_noise_removed, linewidth=0.05, alpha=1, color='#000000')
        
        # # histogram of noise removed plot
        # plt.figure(4)
        # plt.hist(channel_noise_removed, bins=sampling_data * 2)
        # plt.show()

        return channel_noise_removed
    
    def __finding_blank_space(self, channel, sample_rate, save_to_filename=None):
        '''Find noise or a zero blank amplitude'''
        # start to filter blank space [start_index, end_index, streak_counter]
        filtered_zero = []
        start_index = 0
        end_index = 0
        streak_counter = 0

        min_streak = sample_rate // 2

        for i in tqdm(range(len(channel) - 1), desc="Finding noise: "):
            if channel[i] == 0:
                if channel[i + 1] == 0:
                    if start_index == 0:
                        start_index = i
                    streak_counter += 1
                else:
                    if streak_counter >= min_streak:
                        end_index = i
                        filtered_zero.append(
                            [start_index / sample_rate,
                            end_index / sample_rate,
                            streak_counter / sample_rate])

                    # reset temp data
                    start_index = 0
                    end_index = 0
                    streak_counter = 0

        # print(filtered_zero)
        if save_to_filename:
            with open(save_to_filename, 'w', newline='') as file3:
                writer = csv.writer(file3)
                writer.writerow(['start (s)', 'end (s)', 'duration (s)'])
            with open(save_to_filename, 'a', newline='') as file4:
                writer = csv.writer(file4)
                for i in range(len(filtered_zero)):
                    writer.writerow(filtered_zero[i])

        return filtered_zero

    def __trim_timer(self, filtered_array, min_margin=0.5, save_to_filename=None):
        '''Create trimming time'''
        min_threshold_sec = min_margin * 2 + 0.1
        trim_time = []
        tmp_start_time = 0
        for data in filtered_array:
            if data[2] > min_threshold_sec:
                trim_time.append([tmp_start_time, data[0] + min_margin, data[2] - min_margin * 2])
                tmp_start_time = data[1] - min_margin

        if save_to_filename:
            with open(save_to_filename, 'w', newline='') as file5:
                writer = csv.writer(file5)
                writer.writerow(['start (s)', 'end (s)', 'duration (s)'])

            with open(save_to_filename, 'a', newline='') as file6:
                writer = csv.writer(file6)
                for i in range(len(trim_time)):
                    writer.writerow(trim_time[i])

        return trim_time
    
    
    def __create_temp_videos(self, trim_time):
        temp_videos = []
        num_of_parts = len(trim_time)
        for i in tqdm(range(num_of_parts), desc="Trimming {} parts: ".format(num_of_parts)):
            clip = VideoFileClip(self.__original_video_path).subclip(trim_time[i][0], trim_time[i][1])
            temp_filename = 'temp_processing_{}.mp4'.format(i)
            clip.write_videofile(os.path.join(self.__temp_dir, temp_filename), 
                              codec="libx264",
                              temp_audiofile='temp-audio.m4a', 
                              remove_temp=True, 
                              audio_codec='aac',
                              logger=None,
                              verbose=False
                              )
            temp_videos.append(temp_filename)
        
        return temp_videos


    def __create_temp_metadata(self, videos):
        with open(self.__temp_vid_result_metadata, mode='w', newline='') as f:
            for v in videos:
                f.write('file ' + v + '\n')
        
    def __ffmpeg_merge_video(self):
        merge_command = 'ffmpeg -hide_banner -loglevel error -f concat -i {} -c copy {}'.format(
            self.__temp_vid_result_metadata, self.__result_video_path)
        
        code = subprocess.call(merge_command, shell=True)
        # print('Result code: ', code)
        return code

    
    def __create_or_replace_temp_dir(self):
        if os.path.isdir(self.__temp_dir):
            self.__delete_temp_dir()
            
        os.makedirs(self.__temp_dir)
        
        
    def __delete_temp_dir(self):
        shutil.rmtree(self.__temp_dir)
        
    def __delete_wav_audio_path(self):
        os.remove(self.__wav_audio_path)
        
        
    def __create_or_replace_result_file(self):
        if os.path.isfile(self.__result_video_path):
            os.remove(self.__result_video_path)
    
    def auto_trimmer(self, original_video_path:str, result_video_path:str, time_margin_in_second:float=0.50, hist_sampling_data:int=100):
        """Auto trim video to remove audio noise and blank using PodcastPy

        Args:
            original_video_path (str): Original video to be processed
            result_video_path (str): Video result path
            time_margin_in_second (float, optional): Minimum time between the sound gap. Defaults to 0.25 seconds.
            hist_sampling_data (int, optional): Histogram sampling data, used on noise removal process. Defaults to 100.
        """
        start_time = time.time()
        self.__original_video_path = original_video_path
        self.__result_video_path = result_video_path
        
        self.__create_or_replace_temp_dir()
        self.__create_or_replace_result_file()
        
        print("Process 1/8... Opening video...")
        sound = self.__open_video_file()
        
        print("Process 2/8... Extracting audio...")
        channel1, channel2, time_tick = self.__extract_audio_raw_data()

        print("Process 3/8... Audio noise threshold detection...")
        channel_noise_removed = self.__noise_threshold_process(channel1=channel1,
                                            channel2=channel2,
                                            sampling_data=hist_sampling_data,
                                            time_tick=time_tick)

        print("Process 4/8... Audio noise thresold process...")
        filtered_zero = self.__finding_blank_space(
                                        channel=channel_noise_removed,
                                        sample_rate=sound.frame_rate)
        # save_to_filename="filter.csv")  # debugging purpose

        print("Process 5/8... Gathering audio noise time data...")
        time_for_trimming = self.__trim_timer(filtered_array=filtered_zero,
                                    min_margin=time_margin_in_second)
        # save_to_filename="trim.csv")  # debugging purpose

        print("Process 6/8... Trimming video into pieces...")
        temp_videos = self.__create_temp_videos(trim_time=time_for_trimming)
        self.__create_temp_metadata(temp_videos)
        
        print("Process 7/8... Merging video...")
        self.__ffmpeg_merge_video()
        
        print("Process 8/8... Done in {} seconds...".format(time.time() - start_time))
        self.__delete_wav_audio_path()
        self.__delete_temp_dir()