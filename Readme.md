### WasIstDasFuer1Drone 

## Introduction

WasIstDasFuer1Drone was developed for the CDTM elective course “Deep Learning Autonomous Drones” in which student teams of two had 5 days to develop a software that could enable a Parrot AR.Drone 2.0 to (semi-) autonomously fly through a parkour. In our implementation, the drone flies through the parkour, which is made out of three small football goals, by recognising and following the developers’ faces. 

On the final racing day, Friday the 12th of August 2016, WasIstDasFuer1Drone successfully finished the parkour with mind-numbing speed in only 0:33 minutes. The following documentation is meant to give the reader a short overview of the implemented approach, giving insights into the practical application of computer vision and deep learning and hopefully inspiring future students to develop even better algorithms.

## Algorithm and Behaviour

As mentioned above, the core idea behind WasIstDasFuer1Drone is that it should be able to independently detect its creator’s faces so that it can follow them through any given parkour. To accomplish this, an algorithm with three main steps was designed and implemented. 

First of all, Haar feature-based cascade classifiers were used to detect and distinguish human faces. The Haar cascade algorithm is a machine learning based object detection method where a cascade function is trained from a lot of positive and negative images. It is then used to detect objects in other images, in this case faces. For WasIstDasFuer1Drone, many functions of the Open Source Computer Vision (OpenCV) library were utilized, including a relatively straightforward and well-performing implementation of the Haar cascade algorithm. 

Once the drone can distinguish human faces from the environment, it was important to train it in a way that it only follows authorized faces - in this case the developers’. Using the deep learning framework Caffe, several thousand images of authorized and unauthorized faces were used to train a neural network (AlexNet & ImageNet fine tuning) so that it can distinguish one from the other, even in changing environments with varying backgrounds. The results were far from perfect, as there were still many false classifications, but with extensive tweaking they were integrated in a way that the drone could detect authorized faces in a fairly stable manner. Given more time, a better set of training images could have been collected to achieve much better results. 

Finally, having detected an authorized face with a distinct bounding box, the drone now needs to use this geometric information to calculate steering commands. In order to achieve flight in a smooth and precise, a proportional–integral–derivative controller (PID controller) was implemented. 



## Usage

Dependencies:
* pygame
* python-opencv

Start the webserver located in folder webserver/ on localhost or somewhere remote where classification takes place. Then route http traffic via SSH, for instance. A working caffe model you can use to start the server is also in the directory. 

Then just start main.py, wait until you get a camera stream and try steering.


## Steering

The code allows manual steering at any time. The commands are as follows:

Key | Action
--- | ------
RETURN | Takeoff
SPACE | Land
BACKSPACE | Emergency landing (Do not use)
W/A/S/D | Forward, backward, left, right
UP/DOWN | Fly upwards or downwards
0-9 | Drone speed (higher is faster)
u | Activate autonomous mode

Please note that these might not work for operating systems other than OS X.

## Team

Magnus and Jakob are students at the Center for Digital Technologies (CDTM) and the Technical University Munich (TUM). Both are in their Master’s, with Code-Wizard Magnus majoring in Computer Science and Detection-Face Jakob studying Management & Technology. 

