import cv2
import sys

from cvface.detect import FaceDetector


def main():
    input_file = sys.argv[1]
    output_dir = sys.argv[2]

    f = FaceDetector()
    vidcap = cv2.VideoCapture(input_file)
    count = 0
    if not vidcap.isOpened():
        print "not opened"

    success = True
    while success:
        count += 1
        success, image = vidcap.read()
        if count % 2 == 0:
            continue

        output_image = image.copy()
        faces = f.run(image, output_image)
        if len(faces) == 0:
            continue

        for (x,y,w,h) in faces:
            count += 1
            cropped_image = image[y:y+h,x:x+w]
            print 'Read a new frame: ', success
            cv2.imwrite(output_dir + "/frameE%d.jpg" % count, cropped_image)     # save frame as JPEG file

if __name__ == '__main__':
    main()


