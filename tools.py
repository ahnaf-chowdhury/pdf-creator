from PIL import Image, ExifTags
import glob
import os
import cv2
import numpy as np

def save_output(image_list):
    "Saves images in a pdf file in the output folder."
    "If it doesn't exist, it creates one."
    "Renames file for duplicate cases."

    if not os.path.isdir('output_files'):
        os.mkdir('output_files')

    output_name = 'new'

    i = 0
    while os.path.exists(os.path.join('output_files', output_name + '.pdf')):
        if i > 0:
            output_name = output_name[0 : len(output_name)-2]

        i += 1
        output_name = output_name + '_' + str(i)

    image_list[0].save(os.path.join('output_files', output_name + '.pdf'), save_all=True, append_images=image_list[1:])

def preprocess(image, size='a4', portrait=True, dpi=300):
    "preprocesses the image so that it fits a certain page size. image is a PIL image"

    image = rotate_from_metadata(image)

    if not isinstance(image, Image.Image):
        print('ERROR: Item being preprocessed is not a PIL.Image image.')
        return image

    sizes = {'a4': (11.75, 8.25)}   # in inches for portrait orientations
    dimensions = int(sizes[size][0]*dpi), int(sizes[size][1]*dpi)

    if not portrait:     # if a landscape orientation is needed, swap dimensions
        dimensions = dimensions[1], dimensions[0]

    #connvert to numpy array from PIL image:
    im_np = np.array(image)

    #remove alpha layer if there is one:
    if im_np.shape[2] > 3:
        im_np = remove_alpha_numpy(im_np)

    #check aspect ratio and fit on a plank "page":
    aspect_ratio = im_np.shape[1] / im_np.shape[0]    # width/height

    if aspect_ratio < dimensions[1]/dimensions[0]:
        # width comparitively smaller, keep height (= dimensions[0]) and shrink width
        height = dimensions[0]
        width = int(height*aspect_ratio)

        resized_image = cv2.resize(im_np,(width, height))

        final_image = 255*np.ones((dimensions[0], dimensions[1],3), np.uint8)
        final_image[:, (dimensions[1]-width)//2 : (dimensions[1]-width)//2 + width] = resized_image

    else:
        width = dimensions[1]
        height = int(width/aspect_ratio)

        resized_image = cv2.resize(im_np,(width, height))

        final_image = 255*np.ones((dimensions[0], dimensions[1],3), np.uint8)
        final_image[(dimensions[0] - height)//2 : (dimensions[0] - height)//2 + height, :] = resized_image

    return Image.fromarray(final_image)

def rotate_from_metadata(im):
    "rotates PIL image according to metadata"

    try:
        # get metadata
        exif = im._getexif()

        # find key which stores orientation

        for key in ExifTags.TAGS:
            if ExifTags.TAGS[key] == 'Orientation':
                break

        if exif[key] == 3:
            im=im.rotate(180, expand=True)
        elif exif[key] == 6:
            im=im.rotate(270, expand=True)
        elif exif[key] == 8:
            im=im.rotate(90, expand=True)

    except (AttributeError, KeyError, IndexError):
        # image doesn't have getexif
        pass

    return im

def remove_alpha_numpy(image):

    if image.shape[2] > 3:
        image = image[:, :, :3]

    return image

def remove_alpha_pil(image):

    im_np = np.array(image)

    im_np = remove_alpha_numpy(im_np)
    return Image.fromarray(im_np)
