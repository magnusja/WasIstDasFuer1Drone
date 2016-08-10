import cv2
import sys

from cvface.detect import FaceDetector


def main():
    #input_file = sys.argv[1]
    #output_dir = sys.argv[2]

    f = FaceDetector()
    vidcap = cv2.VideoCapture('/media/jakob/data/Projects/Video 10-08-2016, 14 19 36.avi')
    count = 0
    if not vidcap.isOpened():
        print "not opened"

    success = True
    while success:
        count += 1
        success, image = vidcap.read()
        if count % 2 == 1:
            continue

        output_image = image.copy()
        faces = f.run(image, output_image)
        if len(faces) == 0:
            continue

        (x,y,w,h) = faces[0]
        cropped_image = image[y:y+h,x:x+w]
        print 'Read a new frame: ', success
        cv2.imwrite("frame%d.jpg" % count, cropped_image)     # save frame as JPEG file

if __name__ == '__main__':
    main()


