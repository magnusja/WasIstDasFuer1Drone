import cv2


class BatteryOverlay(object):
    def __init__(self, drone):
        self.drone = drone

    def run(self, input):
        battery = self.drone.navdata.get(0, dict()).get('battery', 0)
        cv2.putText(input, 'Battery %f' % battery, (10, 10), cv2.FONT_HERSHEY_PLAIN, 1, (0,255,0), 2)