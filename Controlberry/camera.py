from io import BytesIO
from time import sleep
from picamera import PiCamera
from picamera.exc import PiCameraMMALError

def get_image_as_bytes():
    '''
    returns image as bytes from Pi Camera
    '''
    stream = BytesIO()
    try:
        camera = PiCamera()
        camera.start_preview()
        sleep(1.3)
        camera.capture(stream, format='jpeg')
        stream.seek(0)
        camera.close()
        return stream.getvalue()
    except PiCameraMMALError:
        pass
