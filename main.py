import os


DIR = 'C:/Users/Andy/Stable Diffusion UI/e570a3fa'

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
    for file in files:
        if file.endswith('.txt'):
            set1_txt.add(file[:-4])
        elif file.endswith('.png'):
            # if file contains '_RealESRGAN_x4plus' remove that part
            if '_RealESRGAN_x4plus' in file:
                file = file.replace('_RealESRGAN_x4plus', '')
            set2_png.add(file[:-4])
    return set1_txt, set2_png

def find_missing_files(set1_txt, set2_png):
    # find missing files
    missing_files = set1_txt - set2_png
    return missing_files

def add_txt_extension(missing_files):
    # add .txt extension to missing files
    missing_files_txt = []
    for file in missing_files:
        txt_file = file + '.txt'
        # prepend DIR path to txt_file
        txt_file = os.path.join(DIR, txt_file)
        missing_files_txt.append(txt_file)
    return missing_files_txt

if __name__ == '__main__':
    result = list_files(DIR)
    set1_txt, set2_png = create_two_sets(result)
    # print(result)
    print(set2_png)
    missing_images = find_missing_files(set1_txt, set2_png)
    # print(missing_images)
    bad_txt_files = add_txt_extension(missing_images)
    print(len(bad_txt_files), 'bad txt files')



