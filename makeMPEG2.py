"""
==============================================================================
* California Audiovisual Preservation Project Script: VOB to MPEG2 Converter *
==============================================================================
Description:    Concatenates vob files and creates a .mpg mpeg2 file using ffmpeg.

Note:           This script was originally built as a one-off and not intended for production. However, it should work.
                It just won't be as full featured or as reliable as other scripts.

                There are limitations with this script that'll be known only through use.


Usage:          python makeMPEG2.py [folder]

"""


import argparse
import os
from subprocess import Popen
import shutil
import sys

__author__ = 'California Audio Visual Preservation Project'


# source_path = "/Volumes/CAVPPTestDrive/LAMetroLibrary/"
def make_mpeg2(source_path):
    for root, dirs, files in os.walk(source_path):
        for dir in dirs:
            vobs = []
            print(dir)

            for file in files:
                if file.startswith('.'):
                    pass
                else:
                    if os.path.splitext(file)[1] == ".VOB":
                        if file.startswith("VTS_0"):
                            new_file = os.path.join(root,file)
                            vobs.append(new_file)
            with open(os.path.join(root, "everything.VOB"), 'wb') as complete:
                for filename in vobs:
                    print(filename)
                    shutil.copyfileobj(open(filename, 'rb'), complete)
            # print("Converting {}".format(dir))
            source_vob = os.path.join(root, dir, "everything.VOB")
            destination_mp2 = os.path.join(root, dir, dir + ".mpg")
            # destination_prores = os.path.join(root, dir, dir + ".mov")
            if os.path.exists(source_vob):
                ffmpeg_command = ['ffmpeg', '-v', 'warning', '-stats', '-i', source_vob, '-c:v', 'copy', '-c:a', 'mp2', destination_mp2]
                # ffmpeg_command = ['ffmpeg', '-v', 'warning', '-stats', '-i', source_vob, '-vcodec', 'prores', '-profile:', '3', '-acodec', 'mp2', '-ac', '2',  destination_prores]
                print(" ".join(ffmpeg_command))
                ffmpeg = Popen(ffmpeg_command)
                ffmpeg.communicate()

            # with open(os.path.join(root, "files.txt"), "w") as fileList:
            #     for vob in sorted(vobs):
            #         print(vob)
            #         # print(new_file)
            #         fileList.write("file \'" + vob + "\'\n")


                print("\n")
                print("*****")
            # with open(os.path.join(root, "files.txt"), "r") as newList:

def isValidFolder(folder):
    if os.path.exists(folder) and os.path.dirname(folder):
        return True
    else:
        sys.stderr.write("Invalid argument. Must be a valid folder")
        return False


def main():
    print(__doc__)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('folder', help="Source folder")
    args = parser.parse_args()
    if args.folder:
        if isValidFolder(args.folder):

            print("Extracting VOB")
            make_mpeg2(args.folder)
        else:
            quit(-1)


if __name__ == '__main__':
    main()




