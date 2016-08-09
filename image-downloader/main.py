import io
import logging
import os
import random
import string

import sys
import urllib2
from io import StringIO

import requests
from PIL import Image
from io import BytesIO

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def read_txt(file):
    result = list()
    with open(file) as f:
        for line in f:
            tokens = line.split(' ')
            if float(tokens[6]) > 2:
                logger.info('Found frontal pose')
            else:
                logger.info('Ignoring non frontal pose')
                continue

            box = (int(float(tokens[2])), int(float(tokens[3])), int(float(tokens[4])), int(float(tokens[5])))
            result.append({'url': tokens[1],
                           'box': box})

    return result


def crop_images(images, output_dir):
    for i in images:
        try:
            response = requests.get(i['url'])
            image = Image.open(BytesIO(response.content))
            image = image.crop(i['box'])
            image.save(os.path.join(output_dir, ''.join(random.choice(string.hexdigits) for _ in range(12))) + '.png', format='png')
        except IOError as e:
            logger.error(e)


def main():
    input_file = sys.argv[1]
    output_dir = sys.argv[2]

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    else:
        filelist = [f for f in os.listdir(output_dir)]
        for f in filelist:
            os.remove(os.path.join(output_dir, f))

    images = read_txt(input_file)
    logger.info('Found %d images' % len(images))

    crop_images(images, output_dir)


if __name__ == '__main__':
    main()


