import picamera
import time
import datetime

camera = picamera.PiCamera()



# maximum resolution for pictures is 2592 by 1944
# maximum resolution for videos is 1920 by 1080
camera.resolution = (1920, 1080)

# leave as 15
camera.framerate = 15

# rotation can be 0, 90, 180, or 270 (use 0 for normal)
camera.rotation = 90

# alpha is a number between 0 and 255 (use 255 for normal)
alpha_value = 150

# add a label to your pictures (text size must be between 6 and 160)
camera.annotate_text = " Hello World " 
camera.annotate_text_size = 100
camera.annotate_background = picamera.Color('white')
camera.annotate_foreground = picamera.Color('blue')

# change the brightness and contrast of your pictures (use 50 for normal)
camera.brightness = 50
camera.contrast = 50

# change the camera effects
camera.image_effect = "none"
camera.awb_mode = "auto"
camera.exposure_mode = "auto"



camera.start_preview(alpha = alpha_value)

while 1:

    response = raw_input('Answer: ')

    if response == "p":
        filename = "/home/pi/Desktop/camera/pictures/" + str(datetime.datetime.now()) + ".jpg"
        print("Taking Picture")
        time.sleep(1)
        camera.capture(filename)
        print("Picture Complete")
        print("Filename: " + filename)
        print

    if response == "v":
        filename = "/home/pi/Desktop/camera/videos/" + str(datetime.datetime.now()) + ".h264"
        print("Video Started")
        camera.start_recording(filename)
        time.sleep(6.5)
        print("Video Complete")
        print("Filename: " + filename)
        camera.stop_recording()
        print

    if response == "q":
        camera.stop_preview()
        break
