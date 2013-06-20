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
					 TITLE/ARTIST/ALBUM/YEAR/DURATION/COMMENT of mp3 songs 						 present in a folder.
--------------------------------------------------------------------------------
"""

from shutil import move
from glob import glob
import eyed3
import os

class MakeFolders(object):
	# Initializing info to use for creating folders
	def __init__(self, tag, input_folder):
		self.tag = tag
		self.folder = input_folder
		self.change_cwd()
		self.list_mp3files()
		self.put_songs()

	# Finding song info
	def find_info(self, song_name):
		song_info = dict()
		# Loading Song
		try:
			mp3file = eyed3.load(song_name)
			# Storing all details of song into song_info dictionary
			try:
				song_info['title'] = mp3file.tag.title
			except:
				song_info['title'] = ""
			try:
				song_info['artist'] = mp3file.tag.artist
			except:
				song_info['artist'] = ""
			try:
				song_info['album'] = mp3file.tag.album
			except:
				song_info['album'] = ""
			try:
				song_info['year'] = mp3file.tag.year
			except:
				song_info['year'] = ""
			try:
				song_info['duration'] = mp3file.tag.duration
			except:
				song_info['duration'] = ""
			try:
				song_info['comment'] = mp3file.tag.comment
			except:
				song_info['comment'] = ""
		except:
			song_info = {}
		return song_info
		
	# Changing current working directory to user input folder to access songs
	def change_cwd(self):
		os.chdir(self.folder)
	
	# Checking if required folder exists otherwise create a new one
	def check_folder(self, folder_name):
		if not os.path.exists(folder_name):
			os.mkdir(folder_name)
		
	# Storing list of all .mp3 files
	def list_mp3files(self):
		self.songs = glob('*.mp3')
	
	# Moving song to specific folder
	def move_song(self, song, folder_name):
		try:
			move(song, folder_name)
		except:
			pass

	# Putting all songs in folders according to user choice
	def put_songs(self):
		# Traversing all songs
		for song in self.songs:
			# Calling function to find song info
			song_info = self.find_info(song)
			if song_info != {}:
				folder_name = song_info[self.tag]
				if folder_name in [None, ""]:
					folder_name = "Random"
				self.check_folder(folder_name)
				self.move_song(song, folder_name)
				
# User Choice Menu
menu = "1. TITLE\n2. ARTIST\n3. ALBUM\n4. YEAR\n5. DURATION\n6. COMMENT"
tags = {1: 'title', 2: 'artist', 3: 'album', 4: 'year', 5: 'duration',
		6: 'comment'}

if __name__ == '__main__':
	print "Ensure that mp3fm.py & songs folder should be at same location\n"
	print "'mp3fm' gives you the choice to move songs into folders according \
			to given 6 categories:"
	print menu
	print "\nEnter Songs Folder Name: ",
	input_folder = raw_input()
	print "Enter Number corresponding to above given choices: ",
	tag = tags[input()]
	mp3fm = MakeFolders(tag, input_folder)
	
