#!/usr/bin/env python

"""
==============================================================================
* California Audiovisual Preservation Project Script: VOB to MPEG2 Converter *
==============================================================================
Description: Concatenates vob files and creates an .mpg mpeg2 file using ffmpeg.

Note:        This script was originally built as a one-off and not intended for production. However, it should work.
             It just won't be as full featured or as reliable as other scripts.

             There are limitations with this script that'll be known only through use.


Usage:       python makeMPEG2.py [folder]

"""


import argparse
import os
import subprocess
import shutil
import sys
import re
__author__ = 'California Audio Visual Preservation Project'


TITLE_NUM_PATTERN = re.compile("(?<=VTS_)\d\d")


def get_total_title(source_path):
    total_titles = 0
    for root, dirs, files in os.walk(source_path):
        for file in files:

            # exclude hidden files
            if file.startswith('.'):
                continue

            # exclude files that aren't vobs
            if not os.path.splitext(file)[1] == ".VOB":
                continue

            # exclude files with the wrong prefix
            if not file.startswith("VTS_"):
                continue

            results = int(re.search(TITLE_NUM_PATTERN, file).group(0))
            if results > total_titles:
                total_titles = results
    return total_titles


def get_titles(source_path):
    titles = []
    for root, dirs, files in os.walk(source_path):
        for file in files:

            # exclude hidden files
            if file.startswith('.'):
                continue

            # exclude files that aren't vobs
            if not os.path.splitext(file)[1] == ".VOB":
                continue

            # exclude files with the wrong prefix
            if not file.startswith("VTS_"):
                continue


            titles.append(int(re.search(TITLE_NUM_PATTERN, file).group(0)))
    return set(titles)


def get_vobs_from_title(source_path, title_number):
    vobs = []
    include_hidden = False

    if os.path.exists(source_path):
        for root, dirs, files in os.walk(source_path):
            for file in files:
                if not include_hidden:

                    # exclude hidden files
                    if file.startswith('.'):
                        continue

                # exclude files that aren't vobs
                if not os.path.splitext(file)[1] == ".VOB":
                    continue

                # exclude files with the wrong prefix
                if not file.startswith("VTS_"):
                    continue

                if int(re.search(TITLE_NUM_PATTERN, file).group(0)) == title_number:
                    vobs.append(os.path.join(root, file))

    if len(vobs) > 0:
        return sorted(vobs)


def concat_vobs(new_name, vobs):
    if not vobs:
        raise Exception("Cannot concatenate zero files together.")

    path = os.path.dirname(new_name)
    if not os.path.exists(path):
        os.mkdir(path)

    with open(new_name, 'wb') as complete:
        for filename in vobs:
            print(os.path.basename(filename))
            shutil.copyfileobj(open(filename, 'rb'), complete)
    pass


def make_mpegs(source_path):
    include_hidden = False
    if os.path.exists(source_path):
        for root, dirs, files in os.walk(source_path):
            for file in files:
                if not include_hidden:
                    if file.startswith('.'):
                        continue
                if not os.path.splitext(file)[1] == ".VOB":
                    continue
                print(file)
                new_name = os.path.basename(os.path.splitext(file)[0]) + ".mpg"
                source_file = os.path.join(root, file)
                destination_mp2 = os.path.join(source_path, new_name)

                ffmpeg_command = ['ffmpeg', '-v', 'warning', '-stats', '-i', source_file, '-c:v', 'copy', '-c:a', 'mp2', destination_mp2]
                print(" ".join(ffmpeg_command))
                subprocess.call(ffmpeg_command)


def make_mpeg2(source_path):


    # concatinate titles
    base_name = os.path.basename(source_path)
    destination_path = os.path.join(source_path, "joined")
    print("Sorting", base_name)

    # Find the number of titles
    # total_titles = get_total_title(source_path)
    all_titles = get_titles(source_path)

    titles = []

    # get every chapter with it's title
    for number in all_titles:
        titles.append(get_vobs_from_title(source_path, number))

    # concatenate all the vob files
    for title in titles:
        if title:
            title_number = int(re.search(TITLE_NUM_PATTERN, title[0]).group(0))
            new_name = os.path.join(destination_path, base_name + "_title_" + str(title_number).zfill(2) + ".VOB")
            print("Concatenating " + str(title) + " as " + new_name)
            concat_vobs(new_name, title)


    # print(total_titles)
    print("Making mpeg2 files")
    make_mpegs(destination_path)

    print("All done")


def isValidFolder(folder):
    if os.path.exists(folder) and os.path.dirname(folder):
        return True
    else:
        print(__doc__)
        sys.stderr.write("Invalid argument. Must be a valid folder.\n")
        return False


def main():
    # print(__doc__)
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
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




