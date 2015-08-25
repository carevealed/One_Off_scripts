import os
import shutil

include_hidden = False
source_folder = "/Volumes/DPLA0007"
destination_folder = "/Volumes/DPLA0007/renamed"

files_to_rename = []

if os.path.exists(source_folder):
    for root, dirs, files in os.walk(source_folder):
        if '.' in root:
            continue
        for old_filename in files:
            if not include_hidden:
                if old_filename.startswith('.'):
                    continue
            if os.path.splitext(old_filename)[1] == ".xlsx":
                continue
            files_to_rename.append(os.path.join(root, old_filename))
            # print(os.path.join(root, file))
print("Length is: {}.\n".format(len(files_to_rename)))

prefix = 'cben'


for index, old_filename in enumerate(files_to_rename):

    object_id = prefix + "_" + str(index + 1).zfill(6)
    new_name = object_id +"_prsv"+ os.path.splitext(old_filename)[1]
    new_path = os.path.join(destination_folder, object_id)
    report = ("The original name was {} and was renamed to {}.".format(os.path.basename(old_filename), new_name))
    print(os.path.join(new_path, new_name))
    if not os.path.exists(new_path):
        os.mkdir(new_path)
    shutil.copy2(old_filename, os.path.join(new_path, new_name))
    with open("report.csv", 'a') as f:
        f.write(object_id + "," + report)
        f.write("\n")
    print(report)
    # print(old_filename + "\t -> "+ new_name)

