#/bin/bash

export PYTHONPATH=/root/caffe/python/:$PYTHONPATH

python example.py vgg_face_caffe/VGG_FACE.caffemodel vgg_face_caffe/VGG_FACE_deploy.prototxt vgg_face_caffe/ak.png --nogpu 
