#!/usr/bin/env python

import easygui as eg
import os

class Gui(object):
    """ It handles all GUI related activities """
    def __init__(self):
        """ Defines required variables """
        self.choice = 0
        self.folder = ''
        self.tag = ''

    def folder_choice(self):
        msg = "\t     Welcome to MP3fm!\n\n Select the Songs \
Folder containing Bulk of Songs"
        eg.msgbox(msg, 'MP3fm')
        """ Opens folder choice box and confirm it using index box"""
        fname = eg.diropenbox('Songs Folder', 'Choose', os.getcwd())
        if fname is None:
            exit(0)
        fn = fname[fname.rfind('/')+1:]
        msg = 'Choosen Songs folder:: \t%s' % fn
        options = ('Continue', 'Choose Again', 'Quit')
        ch = eg.indexbox(msg, 'MP3fm', options)
        if ch == 0:
            self.folder = fname
            self.user_choice()
        elif ch == 1:
            self.folder_choice()
        else:
            exit(0)
        return (self.folder, self.choice, self.tag)

    def user_choice(self):
        """ Gives different options to call on Songs """
        fname = self.folder
        fn = fname[fname.rfind('/')+1:]
        msg = 'Choosen Songs folder:: \t%s' % fn
        options = ('Go Back', 'Pack Songs into Folders', 'Unpack all Songs from\
Folders', 'Update Properties(ID3) of songs', 'Quit')
        ch = eg.indexbox(msg, 'MP3fm', options)
        if ch == 0:
            self.folder_choice()
        elif ch == 1:
            msg = 'Choose Tag type'
            options = ('Go Back', 'Album', 'Year', 'Title', 'Artist', 'Quit')
            opt = eg.buttonbox(msg, 'MP3fm', options)
            if opt == 'Go Back':
                self.user_choice()
            elif opt == 'Quit':
                exit(0)
            self.tag = opt
        elif ch == 4:
            exit(0)

        self.choice = ch

    def finish_msg(self):
        ch = self.choice
        if ch == 1:
            msg = 'Songs PACKED Successfully'
        elif ch == 2:
            msg = 'Songs UNPACKED Successfully'
        elif ch == 3:
            msg = 'Songs UPDATED Successfully'

        if(ch == 3):
            options = ('Use Again', 'Quit')
        elif(ch == 2):
            options = ('Use Again', 'View LOG file', 'Delete Empty Folders', \
'Quit')
        else:
            options = ('Use Again', 'View LOG file', 'Quit')

        choice = eg.indexbox(msg, 'MP3fm', options)

        # Importing mp3fm code to run program again
        import mp3fm
        if choice == 0:
            mp3fm.main()

        if choice == 1 and ch == 1:
            msg = 'PackLog File'
            text = open('PackLog.txt').read()
            eg.textbox(msg, 'MP3fm', text)
        elif ch == 2:
            if choice == 1:
                msg = 'UnpackLog File'
                text = open('UnpackLog.txt').read()
                eg.textbox(msg, 'MP3fm', text)
            elif  choice == 2:
                msg = 'Want to Delete Empty Folders left out after Unpacking?'
                opt = eg.ynbox(msg, 'MP3fm')
                if opt == 1:
                    del_folders = []
                    folders = [i for i in os.listdir('.')
                                   if(os.path.isdir(i))]
                    for f in folders:
                        try:
                            os.rmdir(f)
                            del_folders.append(f)
                        except:
                            pass
                    fobj = open('UnpackLog.txt', 'a')
                    fobj.write('\n\n\n*** Empty Folders Removed left out after\
Unpacking ***\n\n\n')
                    for f in del_folders:
                        fobj.write(f+'\n')
                    fobj.close()
                else:
                    self.finish_msg()

                # Options after deleting empty folders
                msg = 'Empty Folders Deleted Successfully'
                options = ('Use Again', 'View LOG file', 'Quit')
                cho = eg.indexbox(msg, 'MP3fm', options)
                if cho == 0:
                    mp3fm.main()
                elif cho == 1:
                    msg = 'Updated UnpackLog File'
                    text = open('UnpackLog.txt').read()
                    eg.textbox(msg, 'MP3fm', text)
        exit(0)
