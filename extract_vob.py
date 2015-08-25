"""
=====================================================================
* California Audiovisual Preservation Project Script: VOB Extractor *
=====================================================================

Description:    Extracts vob files and creates an .iso image.

Note:           This script was originally built as a one-off and not intended for production. However, it should work.
                It just won't be as full featured or as reliable as other scripts.

Usage:          python extract_vob.py [folder]

"""

import os
import subprocess
from time import sleep
import shutil
import argparse
import sys


__author__ = 'California Audio Visual Preservation Project'


# source_path = "/Volumes/CAVPPTestDrive/LAMetroLibrary/"
# program = ['mencoder']
# source_flags = "dvd:// -dvd-device".split()
# destination_flags = "-ovc copy -oac copy -noskip -mc 0 -of mpeg -o ".split()


def extract(source_path):
    if not os.path.exists(source_path):
        print("Path: {} not found".format(source_path))
        exit(-1)

    for root, dir, files in os.walk(source_path):
        for file in files:
            if file.startswith('.'):
                continue
            else:
                base_name, ext = os.path.splitext(file)
                if ext == '.iso':
                    source_iso = os.path.join(root, file)
                    save_path = os.path.join(source_path, base_name)
                    mount_path = os.path.join(save_path, "tmp")
                    mount_command = ["hdiutil", "mount", source_iso, "-mountroot", mount_path]
                    print(source_iso)


                    os.makedirs(save_path)
                    os.makedirs(mount_path)
                    mounter = subprocess.call(mount_command)
                    sleep(1)
                    paths = []
                    for a_root, dir, files in os.walk(mount_path):
                        # print(root)
                        for file in files:
                            if file.startswith('.'):
                                continue
                            else:
                                source_file = os.path.join(a_root, file)
                                destination_file = os.path.join(save_path, file)
                                print("source: {}, destination: {}".format(source_file, destination_file))
                                shutil.copyfile(source_file, destination_file)
                        paths.append(a_root)
                    for b_root in paths:
                        if os.path.exists(b_root):
                            unmount_command = ["hdiutil", "unmount", b_root]
                            print(" ".join(unmount_command))
                            unmounter = subprocess.call(unmount_command)
                    # sleep(10)



                    # unmounter.communicate()
                    print("{}: done".format(base_name))
                    sleep(1)
                    print("***************")


def isValidFolder(folder):
    if os.path.exists(folder) and os.path.dirname(folder):
        return True
    else:
        sys.stderr.write("Invalid argument. Must be a valid folder")
        return False


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('folder', help="Source folder")
    args = parser.parse_args()
    if args.folder:
        if isValidFolder(args.folder):

            print("Extracting VOB")
            extract(args.folder)
        else:
            quit(-1)


if __name__ == '__main__':
    main()




