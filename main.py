from PIL import Image
import glob
import os
import tools
import argparse

if __name__ == "__main__":
    #parse arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("--original_sizes", dest='original_sizes', action="store_true", default=False, help="Keep each page in its original size.")
    args = ap.parse_args()

    KEEP_ORIGINAL_SIZES = args.original_sizes    # keeps the original size of each image/page

    filetypes = ('*.png', '*.jpg', '*jpeg', '*.bmp')

    files = []

    #get paths containing image files
    for type in filetypes:
        files.extend(glob.glob(os.path.join("./input_files", type)))

    if len(files) == 0:
        print('No files of required type found.')
        exit()

    im_list = []
    start = True

    #load files
    for filename in files:
        im = Image.open(filename)
        im_list.append(im)

    # next steps -> add argparse

    if KEEP_ORIGINAL_SIZES:
        # if original sizes are to be kept, images only need to be rotated to their correct
        # orientation using metadata, and alphe channels should be removed (if there)
        for i in range(len(im_list)):
            print('Processing image ' + str(i+1) + 'of ' + str(len(im_list)) + ' ...', end='\r')

            img = im_list.pop(i)
            if 'A' in img.mode.upper():          # if alpha channel exists, remove it
                img = tools.remove_alpha_pil(img)
            img = tools.rotate_from_metadata(img)
            im_list.insert(i, img)

    #if images are to be standardised to a certian dimensions, they need to be preprocessed:
    # (this includes rotation and alpha channel removal as well)
    else:
        for i in range(len(im_list)):
            print('Processing image ' + str(i+1) + 'of ' + str(len(im_list)) + ' ...', end='\r')

            img = im_list.pop(i)
            img = tools.preprocess(img)
            im_list.insert(i, img)

    print('Saving images as a pdf ... ')
    tools.save_output(im_list)

    print('Process complete.')
