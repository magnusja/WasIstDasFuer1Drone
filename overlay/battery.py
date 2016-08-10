import cv2


class BatteryOverlay(object):
    def __init__(self, drone):
        self.drone = drone

    def run(self, input_image, output_image, exec_result=None):
        battery = self.drone.navdata.get(0, dict()).get('battery', 0)
        cv2.putText(output_image, 'Battery %f' % battery, (15, 15), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1)