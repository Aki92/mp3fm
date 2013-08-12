#!/usr/bin/env python

from shutil import move
import pack
import os


class UnpackFolders(pack.PackSongs):
    """
    UnpackFolders class is unpacking all the folders so that all songs comes
    out from folders and reside at one place 
    """
    
    def list_folders(self):
        """ Listing all folders """
        self.folders_to_unpack = [i for i in os.listdir('.') 
                                    if(os.path.isdir(i))]

    def move_song(self, folder_name, song):
        """ Redefining the function which is Moving song to specific folder """
        folder = folder_name
        try:
            # Moving a song from folder to current directory
            move(song, '.')
            # Storing songs list for creating log file
            try:
                self.moved_songs[folder].append(song)
            except:
                self.moved_songs[folder] = [song]
        except:
            # Storing songs list for creating log file
            try:
                self.unmoved_songs[folder].append(song)
            except:
                self.unmoved_songs[folder] = [song]

    def generate_log(self):
        """ 
        Redefining the function which is Generating log according to 
        different types
        """
        prev_songs = self.existing_songs
        moved_songs = self.moved_songs
        unmoved_songs = self.unmoved_songs
        # Opening a log file for
        fh = open('UnpackLog.txt', 'w')
        # Writing previously existing songs in log file
        fh.write('*** Previously existing Songs before unpacking ***\n\n')
        for index,song in enumerate(prev_songs):
            fh.write(str(index)+'. '+str(song)+'\n')
            
        # Writing moved songs in log file
        fh.write('\n\n\n*** Songs MOVED while unpacking ***\n')
        for folder in moved_songs:
            fh.write('\n\n'+str(folder)+':\n')
            for index,song in enumerate(moved_songs[folder]):
                fh.write(str(index)+'. '+str(song)+'\n')
            
        # Writing unmoved songs in log file
        fh.write('\n\n\n*** Songs UNMOVED while unpacking ***\n')
        for folder in unmoved_songs:
            fh.write('\n\n'+str(folder)+':\n')
            for index,song in enumerate(unmoved_songs[folder]):
                fh.write(str(index)+'. '+str(song)+'\n')
    
    def unpack(self):
        """ Running all other functions to unpack folders """
        # Making folders to create log file
        self.existing_songs = self.songs
        self.moved_songs = {}
        self.unmoved_songs = {}
        # Listing all folders inside given folder
        self.list_folders()
        
        # Traversing all folder to unpack them
        for folder in self.folders_to_unpack:
            # Listing all songs under a folder 
            songs = self.list_mp3files(folder)
            # Traversing all songs and moving them
            for song in songs:
                self.move_song(folder, song)
