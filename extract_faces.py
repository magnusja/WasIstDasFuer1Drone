import cv2
import sys
import os

from cvface.detect import FaceDetector



def main():
    #input_file = sys.argv[1]
    #output_dir = sys.argv[2]
    output_dir = "/"

    f = FaceDetector()

    running = True
    while running:
        vidcap = cv2.VideoCapture("/media/jakob/data/Projects/wasistdasfuer1drone/wasistdasfuer1drone.git/small.mp4")

        success,image = vidcap.read()

        #cv2.imshow("image",image)

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


        count = 0
        success = True
        while success:
            success,image = vidcap.read()


            #output_image = image.copy()
            faces = f.run(image, image)
            cropped_image = image[faces]
            print 'Read a new frame: ', success
            cv2.imwrite(output_dir + "/frame%d.jpg" % count, cropped_image)     # save frame as JPEG file
            count += 1

if __name__ == '__main__':
    main()


