import os
from pathlib import Path


# list files in directory and return list
def list_files(directory):
    files = []
    for file in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, file)):
            files.append(file)
    return files


def create_two_sets(files):
    # create two sets of files
    set1_txt = set()
    set2_png = set()
    parts_to_remove = [
        '_RealESRGAN_x4plus',
        '_GFPGANv1.3_RealESRGAN_x4plus',
    ]
    # sort parts_to_remove by length so that larget parts are removed first
    parts_to_remove.sort(key=len, reverse=True)
    for file in files:
        if file.endswith('.txt'):
            set1_txt.add(file[:-4])
        elif file.endswith('.png'):
            for part in parts_to_remove:
                if part in file:
                    file = file.replace(part, '')
            pathObj = Path(file)
            # remove extension
            filename_wo_ext = pathObj.with_suffix('')
            file = str(filename_wo_ext)
            set2_png.add(file)
    return set1_txt, set2_png


def find_missing_files(set1_txt, set2_png):
    # find missing files
    missing_files = set1_txt - set2_png
    return missing_files


def add_dir_root_and_txt_extension(missing_files, dir=None):
    # add .txt extension to missing files
    if not dir:
        raise ValueError('dir is None')
    missing_files_txt = []
    for file in missing_files:
        txt_file = file + '.txt'
        # prepend DIR path to txt_file
        txt_file = os.path.join(dir, txt_file)
        missing_files_txt.append(txt_file)
    return missing_files_txt


if __name__ == '__main__':
    # DIR = 'C:/Users/Andy/Stable Diffusion UI/e570a3fa'
    # DIR = '/Volumes/GoogleDrive-103059428109795353199/My Drive/AI/pics/2022-09-15 e570a3fa red cherries 200'
    DIR = './examples'
    result = list_files(DIR)
    set1_txt, set2_png = create_two_sets(result)
    # print(result)
    print('text files', set1_txt)
    print('png files', set2_png)
    missing_images = find_missing_files(set1_txt, set2_png)
    print('bad orphans', missing_images)
    bad_txt_files = add_dir_root_and_txt_extension(missing_images, dir=DIR)
    print(len(bad_txt_files), 'bad txt files')
