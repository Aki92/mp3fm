MP3fm
=====

"MP3fm" stands for "MP3 Folder Making app" which AUTOMATICALLY pack songs into folders according to user choice from 
TITLE/ARTIST/ALBUM/YEAR/DURATION/COMMENT. It also have a feature of updating song properties i.e. if your songs doesn't 
have its information(ID3 metadata) embedded in it than it would update the song properties automatically from MusicBrainz 
online database.

Features:   
1. **PACK** Songs into folders according to their property (TITLE/ARTIST/ALBUM/YEAR/DURATION/COMMENT).          
2. **UNPACK** Songs back from folders made or you can also unpack songs from already made folders and pack them again using some other song property.        
3. **UPDATE** Song properties using MusicBrainz online database.          
4. **GENERATE LOG** file after every operation, like generate.            



###Instructions to Follow:   

1. Install **mutagen** Tool:    
**`sudo pip install mutagen`**         

2. Install musicbrainzngs Tool:
**`sudo pip install musicbrainzngs`**         

3. Keep **`MP3fm.py`** file with the Folder containing songs.

4. Run the code and follow instructions displayed in it.    
**`python MP3fm.py`**   



