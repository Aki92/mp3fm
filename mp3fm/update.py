#!/usr/bin/env python

import musicbrainzngs as mbz
import pack
import os


class UpdateSongInfo(pack.PackSongs):
    """
    UpdateSongInfo class updates all the songs information using online 
    Music Brainz database.
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
            # Title
            try:
                title = result['title']
                if title != '':
                    info['title'] = title
            except:
                pass
            # Artist name
            try:
                artist = result['artist-credit'][0]['artist']['name']
                if artist != '':
                    info['artist'] = artist
            except:
                pass
            # Album name
            try:
                for res in result['release-list']:
                    if 'title' in res and res['title'] != title:
                        album = res['title']
                        break
                if album != '':
                    info['album'] = album
            except:
                pass
            # Release Year
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
            # Song Length
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
