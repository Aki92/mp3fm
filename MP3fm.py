"""
File Info:
--------------------------------------------------------------------------------
Name: 				mp3fm.py
Libraries Used:     *eyeD3: Finding Song Info(ID3 MetaData)
					(Install using: "sudo pip install eyeD3")
					*glob: Listing all .mp3 files in folders
					*shutil: Moving a file from one place to another
					
Description:		"mp3fm" is an "mp3 folder making app" which AUTOMATICALLY
					 create folders according to user choice from 
					 TITLE/ARTIST/ALBUM/YEAR/DURATION/COMMENT of mp3 songs 						 
					 present in a folder.
--------------------------------------------------------------------------------
"""

import musicbrainzngs as mbz
from shutil import move
from glob import glob
import subprocess
import eyed3
import os

class PackSongs(object):
	# Initializing info to use for creating folders
	def __init__(self, input_folder, tag=''):
		self.tag = tag
		self.folder = input_folder
		self.change_cwd()
		self.list_mp3files()
		
	# Finding song info
	def find_info(self, song_name):
		info = dict()
		# Loading Song
		try:
			mp3file = eyed3.load(song_name)
			# Storing all details of song into "info" dictionary
			try:
				info['title'] = mp3file.tag.title
			except:
				info['title'] = ""
			try:
				info['artist'] = mp3file.tag.artist
			except:
				info['artist'] = ""
			try:
				info['album'] = mp3file.tag.album
			except:
				info['album'] = ""
			try:
				info['year'] = mp3file.tag.best_release_date.year
			except:
				info['year'] = ""
			try:
				info['duration'] = mp3file.info.time_secs * 1000
			except:
				info['duration'] = ""
		except:
			info = {}
		
		self.song_info = info
		
	# Changing current working directory to user input folder to access songs
	def change_cwd(self):
		os.chdir(self.folder)
	
	# Checking if required folder exists otherwise create a new one
	def check_folder(self, folder_name):
		if not os.path.exists(folder_name):
			os.makedirs(folder_name)
		
	# Storing list of all .mp3 files
	def list_mp3files(self, folder=''):
		if folder == '':
			self.songs = glob('*.mp3')
		else:
			return glob(folder+'/*.mp3')
	
	# Moving song to specific folder
	def move_song(self, song, folder_name):
		try:
			move(song, folder_name)
		except:
			pass

	# Generate a log file stating the songs inside each newly created directory
	def generate_log(self):
		# Listing all newly made folders
		new_folders = [i for i in os.listdir('.') if(os.path.isdir(i))]
		# Writing nfo data into log file
		fh = open('PackLog.txt', 'w')
		for folder in new_folders:
			try:
				folder = folder.replace(' ', '\ ')
				nfo = subprocess.check_output('eyeD3 -P nfo %s'%folder, 
											  shell=True)
			except:
				continue
			nfo = nfo[:nfo.find('======')]
			fh.write(nfo+'\n\n\n')
		fh.close()
		
	# Putting all songs in folders according to user choice
	def put_songs(self):
		# Traversing all songs
		for song in self.songs:
			# Calling function to find song info
			self.find_info(song)
			info = self.song_info
			if info != {}:
				folder_name = info[self.tag]
				if folder_name in [None, '', 'Unknown']:
					folder_name = "Random"
				self.check_folder(folder_name)
				self.move_song(song, folder_name)	
	
class UpdateSongInfo(PackSongs):
	# Authenticate the client to query the Music Brainz Server
	def authenticate(self):
		mbz.set_useragent('mp3fm', 1.0, 'akshit.jiit@gmail.com')
		
	def search_musicbrainz(self, song_name):
		info = self.song_info
		if info['title'] in [None, '', 'Unknown'] or 'Track' in info['title']:
			info['title'] = song_name
		self.data = mbz.search_recordings(query=info['title'], limit=1, 
							   artist=info['artist'], release=info['album'],
							   date=info['year'], qdur=info['duration']/2000
							  )
		
	def extract_info(self):
		info = self.song_info
		data = self.data
		try:
			title = data['recording-list'][0]['title']
			if title != '':
				info['title'] = title
		except:
			pass
		try:
			artist = data['recording-list'][0]['artist-credit'][0]['artist']\
																    ['name']
			if artist != '':
				info['artist'] = artist
		except:
			pass
		try:
			album = data['recording-list'][0]['release-list'][0]['title']
			if album != '':
				info['album'] = album
		except:
			pass
		try:
			year = data['recording-list'][0]['release-list'][0]['date']
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
		# Updating old song info with new info found from net
		self.song_info = info
		
	# Saving new song info
	def save_info(self, song_name):
		# Loading new changed song info
		info = self.song_info
		# Loading Song
		try:
			mp3file = eyed3.load(song_name)
			# Storing all details of song into song_info dictionary
			try:
				mp3file.tag.title = info['title']
			except:
				mp3file.tag.title = ""
			try:
				mp3file.tag.artist = info['artist'] 
			except:
				mp3file.tag.artist = ""
			try:
				mp3file.tag.album = info['album']
			except:
				mp3file.tag.album = ""
			try:
				mp3file.tag.best_release_date.year = info['year']
			except:
				mp3file.tag.best_release_date.year = ""
		except:
			pass
		
		try:			
			# Saving new info back to song properties
			mp3file.tag.save()
		except:
			pass
		
	def update_id3(self):
		self.authenticate()
		for song in self.songs:
			self.find_info(song)
			if self.song_info != {}:
				self.search_musicbrainz(song)
				self.extract_info()
				self.save_info(song)

class UnpackFolders(PackSongs):
	# Listing all folders 
	def list_folders(self):
		self.folders_to_unpack = [i for i in os.listdir('.') 
								     if(os.path.isdir(i))]

	# Redefining the function which is Moving song to specific folder
	def move_song(self, folder_name, song):
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

	# Redefining the function which is Generating log according to diff. types
	def generate_log(self):
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
		fh.write('\n\n\n\n*** Songs MOVED while unpacking ***\n')
		for folder in moved_songs:
			fh.write('\n\n'+str(folder)+':\n')
			for index,song in enumerate(moved_songs[folder]):
				fh.write(str(index)+'. '+str(song)+'\n')
			
		# Writing unmoved songs in log file
		fh.write('\n\n\n\n*** Songs UNMOVED while unpacking ***\n')
		for folder in unmoved_songs:
			fh.write('\n\n'+str(folder)+':\n')
			for index,song in enumerate(unmoved_songs[folder]):
				fh.write(str(index)+'. '+str(song)+'\n')
				
	def unpack(self):
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
	# User Choice Menu
	options = "1. Pack Songs into Folders.\n2. Unpack all Songs from Folders\n\
3. Update Properties(ID3) of songs.\nEnter Choice:"
	menu = "1. TITLE\n2. ARTIST\n3. ALBUM\n4. YEAR\n5. DURATION\n6. COMMENT"
	tags = {1: 'title', 2: 'artist', 3: 'album', 4: 'year', 5: 'duration',
			6: 'comment'}

	print("Ensure that mp3fm.py & songs folder should be at SAME location\n")
	
	print("\nEnter Folder's Name containing all songs: ")
	input_folder = raw_input()
	
	print(options)
	choice = input()
	
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