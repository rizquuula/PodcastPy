"""
Created on Fri 02 15:03:00 2022
@license: MIT License
@author: eiproject (https://github.com/eiproject)

"""
from pydub import AudioSegment
from moviepy.editor import VideoFileClip, concatenate_videoclips
import os
import csv
import time
import scipy.io.wavfile
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

class PodcastPy:
    def __init__(self):
        self.__title__ = 'PodcastPy'
        self.__description__ = 'Podcast Automation Tools'
        self.__original_video_path = None
        self.__result_video_path = None
        
    def __open_video_file(self):
        '''Open audio from video file using pydub'''
        sound = AudioSegment.from_file(self.__original_video_path)
        return sound    
    
    def __extract_audio_raw_data(self):
        '''Extract the audio to a .wav file'''
        wav_filename = os.path.splitext(os.path.basename(self.__original_video_path))[0] + '.wav'
        AudioSegment.from_file(self.__original_video_path).export(wav_filename, format='wav')

        # read wav file using scipy
        rate, audData = scipy.io.wavfile.read(wav_filename)

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
    
    
    def __noise_removal(self, channel1, channel2, hist_sampling_data):
        channel_concat = np.int16(np.mean(np.array([np.int32(channel1), np.int32(channel2)]), axis=0))
        sampling_data = hist_sampling_data

        # # stereo plot
        # plt.figure(1)
        # plt.plot(time_tick, channel1, linewidth=0.05, alpha=1, color='#000000')
        # plt.plot(time_tick, channel2, linewidth=0.05, alpha=1, color='#ff0000')

        # # histogram plot
        # plt.figure(2)
        counts, bins, bars = plt.hist(np.abs(channel_concat), bins=sampling_data * 2)

        # finding threshold value
        threshold_val = bins[sampling_data + 1]
        channel_noise_removed = np.int16(
            np.where((-threshold_val < channel_concat) & (channel_concat < threshold_val), 
                     0, 
                     channel_concat))

        # # noise removed plot
        # plt.figure(3)
        # plt.plot(time_tick, channel_noise_removed, linewidth=0.05, alpha=1, color='#000000')
        #
        # # histogram of noise removed plot
        # plt.figure(4)
        # plt.hist(channel_noise_removed, bins=sampling_data * 2)

        return channel_noise_removed
    
    def __filter_blank_space(self, channel, sample_rate, save_to_filename=None):
        # start to filter blank space [start_index, end_index, streak_counter]
        filtered_zero = []
        start_index = 0
        end_index = 0
        streak_counter = 0

        min_streak = sample_rate // 2

        for i in tqdm(range(len(channel) - 1)):
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
        # good for trim
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
    
    
    def __auto_trim_and_merge(self, trim_time):
        clip_array = []
        print("Auto trimmer processing {} video parts".format(len(trim_time)))
        for i in tqdm(range(len(trim_time))):
            clip = VideoFileClip(self.__original_video_path).subclip(trim_time[i][0], trim_time[i][1])

            # clip.to_videofile('res{}.mp4'.format(i), codec="libx264",
            #                   temp_audiofile='temp-audio.m4a', remove_temp=True, audio_codec='aac')
            clip_array.append(clip)

        final = concatenate_videoclips(clip_array)
        final.write_videofile(self.__result_video_path)


    def main(self, original_video_path:str, result_video_path:str, time_margin_in_second:float=0.25, hist_sampling_data:int=100):
        """Main function to work with PodcastPy

        Args:
            original_video_path (str): Original video to be processed
            result_video_path (str): Video result path
            time_margin_in_second (float, optional): Minimum time between the sound gap. Defaults to 0.25 seconds.
            hist_sampling_data (int, optional): Histogram sampling data, used on noise removal process. Defaults to 100.
        """
        start_time = time.time()
        self.__original_video_path = original_video_path
        self.__result_video_path = result_video_path
        
        print("Process 1/7... Opening video...")
        sound = self.__open_video_file()
        
        print("Process 2/7... Extracting audio...")
        channel1, channel2, time_tick = self.__extract_audio_raw_data()

        print("Process 3/7... Audio noise removal...")
        channel_noise_removed = self.__noise_removal(channel1=channel1,
                                            channel2=channel2,
                                            hist_sampling_data=hist_sampling_data)

        print("Process 4/7... Audio filter zero space...")
        filtered_zero = self.__filter_blank_space(
                                        channel=channel_noise_removed,
                                        sample_rate=sound.frame_rate)
        # save_to_filename="filter.csv")  # debugging purpose

        print("Process 5/7... Calculating trim time from audio...")
        time_for_trimming = self.__trim_timer(filtered_array=filtered_zero,
                                    min_margin=time_margin_in_second)
        # save_to_filename="trim.csv")  # debugging purpose

        print("Process 6/7... Trim and merge video...")
        self.__auto_trim_and_merge(trim_time=time_for_trimming)

        print("Process 7/7... Done in {} seconds...".format(time.time() - start_time))