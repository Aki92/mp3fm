#!/usr/bin/env python

from Tkinter import *
from thread import *
import unpack
import update
import pack
import gui
import sys
import os

__mp3fm_version__ = '1.0.1'


def main():
    """
    Main function which is asking user for choices and making appropriate
    class objects and calling appropriate functions corresponding to them
    """
    # Calling folder selection and choice selection boxes
    obj = gui.Gui()
    input_folder, choice, stag = obj.folder_choice()
    global err
    err = 0

    if choice == 1:
        tag = stag.lower()
        mp3fm = pack.PackSongs(input_folder, tag)
        mp3fm.put_songs()
        mp3fm.generate_log()
    elif choice == 2:
        mp3fm = unpack.UnpackFolders(input_folder)
        mp3fm.unpack()
        mp3fm.generate_log()
    elif choice == 3:
        mp3fm = update.UpdateSongInfo(input_folder)
        #mp3fm.update_id3() 
        # GUI to show a message till songs properties update
        def stop(root, mp3fm):
            global err
            err = mp3fm.update_id3()
            root.quit()

        root = Tk()
        txt = Text(root, width=40, height=5)
        txt.insert(INSERT, "Please Wait! Songs are Updating...")
        txt.pack()
        # Running stop function in background so that it can stop the display msg
        start_new_thread(stop, (root, mp3fm, ))
        root.mainloop()
        root.destroy()

    if err == 1:
        # Exiting the program as Internet not working
        exit()
    # Calling finish msg prompt
    obj.finish_msg()

if __name__ == '__main__':
    args = sys.argv[0:]
    if args in ('-v', '--version'):
        print(__mp3fm_version__)
    elif args in ('-h', '--help'):
        print('''-h: Help
                -v: mp3fm Version
                Run the code directly by typing mp3fm without any arguments
              '''
             )
    while main() == 1:
        continue
