#!/usr/bin/env python

from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
import musicbrainzngs as mbz
from shutil import move
from glob import glob
import os

class PackSongs(object):
    """
    It pack songs into folders according to property choosen by the user
    making easy to manage songs and keep them into folders
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
    
    def check_folder(self, folder_name):
        """ Checking if required folder exists otherwise create a new one """
        if not os.path.exists(folder_name):
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
            text = 'Folder	:	' + folder + '\n' + "-"*(12+len(folder)) + \
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

class UpdateSongInfo(PackSongs):
    """
    It updates all the songs information using online Music Brainz database.
    """
    def authenticate(self):
        """ Authenticate the client to query the Music Brainz Server """
        mbz.set_useragent('mp3fm', 1.0, 'akshit.jiit@gmail.com')
        
    def search_musicbrainz(self, song_name):
        """ Searching music brainz db for particular song """
        info = self.song_info
        if info['title'] == '' or 'Track' in info['title']:
            # Converting song_name into lower case so that we don't have to 
            # search for all .MP3 combination like(mp3,mP3,Mp3,MP3)
            song_name = song_name.lower()
            if '.mp3' in song_name:
                pos = song_name.find('.mp3')
            info['title'] = song_name[:pos]
            
        # Finding song information in DB of music brainz and taking only 1
        # result in response by using limit=1
        self.data = mbz.search_recordings(query=info['title'], limit=1, 
                            artist=info['artist'], release=info['album'],
                            date=str(info['year']), qdur=str(info['duration'])
                            )
    
    def extract_info(self):
        """ Extracting information from result found in above function """
        info = self.song_info
        data = self.data
        if data['recording-list'] != []:			
            result = data['recording-list'][0]
            try:
                title = result['title']
                if title != '':
                    info['title'] = title
            except:
                pass
            try:
                artist = result['artist-credit'][0]['artist']['name']
                if artist != '':
                    info['artist'] = artist
            except:
                pass
            try:
                for res in result['release-list']:
                    if 'title' in res and res['title'] != title:
                        album = res['title']
                        break
                if album != '':
                    info['album'] = album
            except:
                pass
            try:
                for res in result['release-list']:
                    if 'date' in res:
                        date = res['date'].split('-')
                        year = [i for i in date if len(i)==4][0]
                        break
                if year != '':
                    info['year'] = year
            except:
                pass
            try:
                dur = data['recording-list'][0]['length'] / 1000
                if dur != '':
                    info['duration'] = dur
            except:
                pass
        else:
            info = {}
        # Updating old song info with new info found from net
        self.song_info = info
    
    def convert_to_unicode(self, string):
        """ Converting string into unicode string using UTF-8 format """
        return string.decode('utf-8')
        
    def save_info(self, song_name):
        """ Saving new song info """
        # Loading new changed song info
        info = self.song_info
        # Loading Song
        try:
            # Updating title of song
            try:
                self.mp3file['title'] = self.convert_to_unicode(info['title'])
            except:
                pass
            # Updating artist of song
            try:
                self.mp3file['artist'] = self.convert_to_unicode(info['artist'])
            except:
                pass
            # Updating song album
            try:
                self.mp3file['album'] = self.convert_to_unicode(info['album'])
            except:
                pass
            # Updating release_date of song
            try:
                self.mp3file['date'] = self.convert_to_unicode(info['year'])
            except:
                pass
        except:
            pass
        
        try:			
            # Saving new info back to song properties
            self.mp3file.save()
        except:
            pass

        # Updating song name to title of song
        try:
            if info['title'] != '':
                os.rename(song_name, info['title']+'.mp3')
        except:
            pass
    
    def update_id3(self):
        """ Function calling all other functions to update song info """
        self.authenticate()
        for song in self.songs:
            self.find_info(song)
            if self.song_info != {}:
                self.search_musicbrainz(song)
                self.extract_info()
                self.save_info(song)

class UnpackFolders(PackSongs):
    """
    It unpacks all the folders so that all songs comes out from folders and
    reside at one place 
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
                
def main():
    """
    Main function which is asking user for choices and making appropriate 
    class objects and calling appropriate functions corresponding to them
    """
    # User Choice Menu
    options = "1. Pack Songs into Folders.\n2. Unpack all Songs from Folders\n\
3. Update Properties(ID3) of songs.\nEnter Choice:"
    menu = "1. TITLE\n2. ARTIST\n3. ALBUM\n4. YEAR\n5. DURATION\n6. COMMENT"
    tags = {1: 'title', 2: 'artist', 3: 'album', 4: 'year', 5: 'duration',
            6: 'comment'}

    print(options)
    choice = input()
    
    # Input folder would be the folder which contains all songs.
    input_folder = os.getcwd()
    
    if choice == 1:
        print("'mp3fm' gives you the choice to move songs into folders \
according to given 6 categories:")
        print(menu)
        print "Enter Number corresponding to above given choices: ",
    
        tag = tags[input()]
        mp3fm = PackSongs(input_folder, tag)
        mp3fm.put_songs()
        mp3fm.generate_log()
        
        print("*** Folders made with a LOG file containing Songs Info. \
present in every folder ***")

    elif choice == 2:
        mp3fm = UnpackFolders(input_folder)
        mp3fm.unpack()
        mp3fm.generate_log()

    elif choice == 3:
        mp3fm = UpdateSongInfo(input_folder)
        mp3fm.update_id3()
            
            
if __name__ == '__main__':
    main()