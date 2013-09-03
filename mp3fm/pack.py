#!/usr/bin/env python

from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from shutil import move
from glob import glob
import os


class PackSongs(object):
    """
    PackSongs pack songs into folders according to property choosen
    by the user making easy to manage songs and keep them into folders
    """
    
    def __init__(self, input_folder, tag=''):
        """ Initializing info to use for creating folders """
        self.tag = tag
        self.folder = input_folder
        self.change_cwd()
        self.list_mp3files()
        
    def find_info(self, song_name):
        """ Finding song info """
        info = dict()
        # Loading Song
        try:
            self.mp3file = MP3(song_name, ID3=EasyID3)
            # Storing all details of song into "info" dictionary
            try:
                info['title'] = str(self.mp3file['title'][0])
            except:
                info['title'] = ''
            try:
                info['artist'] = str(self.mp3file['artist'][0])
            except:
                info['artist'] = ''
            try:
                info['album'] = str(self.mp3file['album'][0])
            except:
                info['album'] = ''
            try:
                info['year'] = str(self.mp3file['date'][0])
            except:
                info['year'] = ''
            try:
                info['duration'] = int(self.mp3file.info.length * 1000)
            except:
                info['duration'] = ''
        except:
            info = {}
        
        self.song_info = info
        
    def change_cwd(self):
        """ 
        Changing current working directory to user input folder to access songs
        """
        os.chdir(self.folder)

    def remove_schars(self, fn, char):
        """ Removing special chars from folder name """
        fl = 0
        while fl != 1:
            try:
                fn.remove(char)
            except:
                fl = 1
        return fn
    
    def check_folder(self, folder_name):
        """ Checking if required folder exists otherwise create a new one """
        if not os.path.exists(folder_name):
            try:
                os.makedirs(folder_name)
            except:
                fn = list(folder_name)
                special_chars = [':', '/', '\\', '*', '?', '<', '>', '|']
                for i in special_chars:
                    fn = self.remove_schars(fn, i)
                folder_name = ''.join(fn)
                os.makedirs(folder_name)
        
    def list_mp3files(self, folder=''):
        """ Storing list of all .mp3 files """
        # All posibilities of writing mp3 considered ;)
        if folder == '':
            self.songs = glob('*.??3')
        else:
            return glob(folder+'/*.??3')
    
    def move_song(self, song, folder_name):
        """ Moving song to specific folder """
        try:
            move(song, folder_name)
        except:
            pass

    def generate_log(self):
        """ 
        Generate a log file stating the songs inside each newly created
        directory
        """
        # Listing all newly made folders
        new_folders = [i for i in os.listdir('.') if(os.path.isdir(i))]
        # Writing nfo data into log file
        fh = open('PackLog.txt', 'w')
        for folder in new_folders:
            text = 'Folder  :   ' + folder + '\n' + "-"*(12+len(folder)) + \
            '\n\n' + 'Track Listing' + '\n' + "-"*len('Track Listing') + '\n'
            try:
                songs = os.listdir(folder)
                for index,name in enumerate(songs):
                    text += str(index+1) + '. ' + name + '\n'
            except:
                continue
            fh.write(text+'\n\n\n')
        fh.close()
        
    def put_songs(self):
        """ Putting all songs in folders according to user choice """
        # Traversing all songs
        for song in self.songs:
            # Calling function to find song info
            self.find_info(song)
            info = self.song_info
            if info != {}:
                folder_name = info[self.tag]
                if folder_name in [None, '', 'Unknown']:
                    folder_name = 'Random'
                self.check_folder(folder_name)
                self.move_song(song, folder_name)   
