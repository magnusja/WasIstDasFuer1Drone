import io
import logging
import os
import random
import string

import sys
from functools import partial

import multiprocessing
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

            if len(result) > 100:
                break

    return result


def crop_image(i, output_dir):
    try:
        response = requests.get(i['url'])
        image = Image.open(BytesIO(response.content))
        image = image.crop(i['box'])
        image.save(os.path.join(output_dir, ''.join(random.choice(string.hexdigits) for _ in range(12))) + '.png', format='png')
    except IOError as e:
        logger.error(e)


def main():
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    else:
        filelist = [f for f in os.listdir(output_dir)]
        for f in filelist:
            os.remove(os.path.join(output_dir, f))

    filelist = [f for f in os.listdir(input_dir) if f.endswith('.txt')]

    images = list()
    for f in filelist:
        logger.info('Reading file %s', f)
        images.extend(read_txt(os.path.join(input_dir, f)))

    logger.info('Found %d images' % len(images))

    pool = multiprocessing.Pool(processes=64)
    pool.map(partial(crop_image, output_dir=output_dir), images)


if __name__ == '__main__':
    main()


