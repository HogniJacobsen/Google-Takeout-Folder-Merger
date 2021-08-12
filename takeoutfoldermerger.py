import shutil
import os
from tkinter import filedialog
from tkinter import *
import sys

class MergeFolders:
    def __init__(self): # home_directory
        # self.home_directory = home_directory
        self.folders = []
        self.skipped = []
        self.moved_history = dict()
        self.length_files = 0
        self.length_folders = 0

    def select_folder(self, title):
        root = Tk()
        root.withdraw()
        return filedialog.askdirectory(title = title) # initialdir = self.home_directory, 

    def destination_folder(self):
        self.dst_folder = self.select_folder(title = 'Select destination folder')

    def source_folder(self):
        folder = 0
        while True:
            if folder == '':
                break
            folder = self.select_folder(title = 'Select a source folder')
            self.folders.append(folder)

    def length_of_files_folders(self):
        for directory in self.folders:
            for walk in os.walk(directory, topdown=True):
                self.length_files += len(walk[2])
                self.length_folders += len(walk[1])

    def move_photos(self):
        if self.length_files == 0 and self.length_folders == 0:
            self.length_of_files_folders()
        count_files = 0
        count_folders = 0
        for directory in self.folders:
            for walk in os.walk(directory, topdown=True):
                # Make new folders
                for folder in walk[1]:
                    count_folders += 1
                    new_folder = f'{walk[0].replace(directory, self.dst_folder)}/{folder}'
                    if os.path.isdir(new_folder):
                        pass
                    else:
                        try: 
                            if folder[0] != '.': # To ignore APFS .ds_store files and folders.
                                os.mkdir(new_folder)
                        except OSError as err:
                            sys.stdout.write(f'\r {str(err)}')
                            sys.stdout.flush()
                    sys.stdout.write(f'\r Folder creation: {round((count_folders/self.length_folders)*100)}%')
                    sys.stdout.flush()
                # Move files.
                move_path = walk[0].replace(directory, self.dst_folder)
                if len(walk) == 3:
                    for file in walk[2]:
                        count_files += 1
                        if file[0] != '.': # To ignore APFS .ds_store files and folders.
                            try:
                                self.moved_history[f'{walk[0]}/{file}'] = move_path
                                shutil.move(f'{walk[0]}/{file}', move_path)
                            except OSError as err:
                                sys.stdout.write(f'\r {str(err)}')
                                sys.stdout.flush()
                                self.skipped.append(file)
                        sys.stdout.write(f'\r Moving files: {round((count_files/self.length_files)*100)}%')
                        sys.stdout.flush()
        if len(self.skipped) > 0:
            sys.stdout.write(f'\r {len(self.skipped)} files skipped.')
            sys.stdout.flush()
 
if __name__ == '__main__':
    test = MergeFolders()
    print('\r Select a destination folder.')
    test.destination_folder()
    print('\r Select a source folder/s or Cancel to continue.')
    test.source_folder()
    start_merger = input('\r Start merger? Type YES to continue: ')
    if start_merger == 'YES':
        test.move_photos()
    else:
        print('Stopped')