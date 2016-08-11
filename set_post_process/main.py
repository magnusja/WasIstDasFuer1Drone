import os
import random
import sys

import multiprocessing

from PIL import Image


def process_image(image_path):
    # rotate
    image = Image.open(image_path)
    for i in range(0, 4):
        image.rotate(random.randrange(-30, 30)).save(image_path + 'rot' + str(i) + '.jpg', 'JPEG')
    # mirror
    # change color space
    pass


def main():
    input_folder = sys.argv[1]

    filelist = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if not f.startswith('.')]

    reduced_file_list = [random.choice(filelist) for i in range(0, 300)]

    pool = multiprocessing.Pool(processes=4)
    pool.map(process_image, reduced_file_list)

if __name__ == '__main__':
    main()
