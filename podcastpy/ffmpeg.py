from .cmd import try_cmd, subprocess_call

import os
import subprocess

class FFMPEG:
    """
    FFMPEG adapter using subprocess
    @author: M Razif Rizqullah (https://github.com/eiproject)
    @created_at: Tue, Feb 08 2022. 13:40
    """
    def __init__(self, log_level='error'):
        self.__title__ = "FFMPEG Adapter"
        
        self.ffmpeg_binary = None
        self.log_level = log_level
        
        self.__auto_detect_ffmpeg_binary()

    
    def set_binary(self, binary_path:str):
        '''Manually set FFMPEG binary file'''
        if self.__is_valid_ffmpeg_binary(binary_path):
            self.ffmpeg_binary = binary_path
        
    
    def is_media_supported(self, filename:str):
        commands = [self.ffmpeg_binary,
                    '-i',filename, '-f null /dev/null']
        
        cmd = ' '.join(commands)
        stderrdata, is_errors = subprocess_call(cmd)
        return is_errors
    
    
    def merge_media(self, metadata:str, output_path:str):
        """
        Merge media parts using a metadata in a text file

        Args:
            metadata (str): Metadata file, consist `file filename.format`
            output_path (str): Output path

        Returns:
            (int): Subprocess code
        """
        if not self.__is_available_ffmpeg_binary(): return -1
        
        commands = [self.ffmpeg_binary,
                    '-hide_banner',
                    '-loglevel', 'error',
                    '-f', 'concat',
                    '-i', metadata,
                    '-c', 'copy',
                    output_path]
        
        cmd = ' '.join(commands)
        stderrdata, is_errors = subprocess_call(cmd)
        return is_errors

    def split_media(self, original_path:str, start:float, end:float, output_path:str):
        """
        Split a media using start and end time in (float) seconds

        Args:
            original_path (str): Source media
            start (float): Start time
            end (float): End time
            output_path (str): Output path

        Returns:
            (int): Subprocess code
        """
        if not self.__is_available_ffmpeg_binary(): return -1
        
        commands = [self.ffmpeg_binary, 
                    '-y', '-hide_banner', 
                    '-loglevel', 'error', 
                    '-ss', "%0.2f"%start, 
                    '-i', original_path, 
                    '-t', "%0.2f"%(end - start), 
                    '-map', '0', 
                    '-vcodec', 'copy', 
                    '-acodec', 'copy', 
                    output_path]
        
        cmd = ' '.join(commands)
        stderrdata, is_errors = subprocess_call(cmd)
        return is_errors
    
    
    def __auto_detect_ffmpeg_binary(self):
        '''Checking FFMPEG binary file configuration'''
        if try_cmd(['ffmpeg'])[0]:
            self.ffmpeg_binary = 'ffmpeg'
        elif try_cmd(['ffmpeg.exe'])[0]:
            self.ffmpeg_binary = 'ffmpeg.exe'
        else:
            self.ffmpeg_binary = None
    
    
    def __is_available_ffmpeg_binary(self):
        '''Checking current FFMPEG binary status'''
        if self.ffmpeg_binary is None: 
            print('''
                  There is no FFMPEG binary found on your machine.\n 
                  Please add it to a path or set ir manually using set_binary() function
                  ''')
            return False
        return True
    
    
    def __is_valid_ffmpeg_binary(self, binary_path):
        '''Is current FFMPEG binary valid'''
        if not os.path.isfile(binary_path):
            print('''FFMPEG binary path is not found.''')
            
        elif try_cmd([binary_path])[0]:
            return True
        
        else:
            print('''FFMPEG binary path is invalid.''')
        
        return False