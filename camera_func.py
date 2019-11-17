

from picamera import PiCamera
from time


def take_picture(name):

	memory = '/home/pi/Desktop/criclass/'
	camera = PiCamera()
	camera.start_preview()
	sleep(5)
	camera.capture(memory + name)
	camera.stop_preview()
