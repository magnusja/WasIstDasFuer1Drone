import cv2
import sys
import os

from cvface.detect import FaceDetector



def main():
    input_file = sys.argv[1]
    output_dir = sys.argv[2]

    f = FaceDetector()

    running = True
    while running:
        vidcap = cv2.VideoCapture(input_file)
        success,image = vidcap.read()
        count = 0
        success = True
        while success:
            success,image = vidcap.read()
            output_image = image.copy()
            faces = f.run(image, output_image)
            (x,y,w,h) = faces[0]
            cropped_image = image[y:y+h,x:x+w]
            print 'Read a new frame: ', success
            cv2.imwrite(output_dir + "frame%d.jpg" % count, cropped_image)     # save frame as JPEG file
            count += 1

if __name__ == '__main__':
    main()


